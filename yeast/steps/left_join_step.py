from pandas.core.frame import DataFrame
from yeast import Recipe
from yeast.step import Step
from yeast.errors import YeastValidationError


class LeftJoinStep(Step):
    """
    Return all rows from `Left`, and all columns from `Left` and `Right`.
    Rows in `Left` with no match in `Right` will have NA values in the new columns.
    If there are multiple matches between `Left` and `Right` all combinations of the matches
    are returned.

    Parameters:

    - `right`: DataFrame or Recipe to merge with.
    - `by`: optional colum name list to merge by. Default: None
    - `df`: optional df to be used as input if right is a Recipe

    Usage:

    ```python
    # Left Join with another DataFrame
    # sales_df and client_df are DataFrames, by argument is optional
    Recipe([
        LeftJoinStep(sales_df, by="client_id")
    ]).bake(client_df)

    # Left join with the DataFrame obtained from the execution of a Recipe
    # sales_recipe will be executed using sales_df inside the client_recipe execution
    sales_recipe = Recipe([
        RenameStep({'client_id': 'cid'})
    ])

    client_recipe = Recipe([
        LeftJoinStep(sales_recipe, by=["client_id", "region_id"], df=sales_df)
    ])

    client_recipe.prepare(client_df).bake(client_df)
    ```

    Raises:

    - `YeastValidationError`: if any of the validations is not correct.
    """
    def __init__(self, right, by=None, df=None):
        self.right = right
        self.by = by if not by else by if type(by) in [list, tuple] else [by]
        self.df = df

    def do_prepare(self, left):
        # Prepare the Recipe before Merges
        if isinstance(self.right, Recipe):
            self.right = self.right.prepare(self.df)

    def do_bake(self, left):
        if isinstance(self.right, Recipe):
            self.right = self.right.bake(self.df)
        return left.merge(self.right, how="left", on=self.by, suffixes=['_x', '_y'])

    def do_validate(self, left):
        """
        - We are expecting DataFrame or Recipe on Right
        - Left must be a DataFrame
        - All columns in by must be on Left
        - All columns in by must be on Right
        - df is only supported if right is a Recipe
        """
        # We are expecting DataFrame or Recipe on Right
        if not isinstance(self.right, DataFrame) and not isinstance(self.right, Recipe):
            raise YeastValidationError('We are expecting a DataFrame or a Recipe or Right')
        # Left must be a DataFrame
        if not isinstance(left, DataFrame):
            raise YeastValidationError("Previous Step didn't return a DataFrame")
        # All columns in by must be on Left
        if self.by:
            missing = [c for c in self.by if c not in left.columns]
            if missing:
                raise YeastValidationError(
                    f"Columns {missing} not found on the left side of the merge"
                )
        # All columns in by must be on Right
        if self.by and isinstance(self.right, DataFrame):
            missing = [c for c in self.by if c not in self.right.columns]
            if missing:
                raise YeastValidationError(
                    f"Columns {missing} not found on the right side of the merge"
                )
        # self.df is only supported if right is a Recipe
        if self.df is not None and not isinstance(self.right, Recipe):
            raise YeastValidationError(f"'df' parameter is only supported if right is a Recipe")
