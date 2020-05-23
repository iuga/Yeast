from pandas.core.frame import DataFrame
from yeast import Recipe
from yeast.step import Step
from yeast.errors import YeastValidationError


class JoinStep(Step):
    """
    Join two DataFrames together

    The steps join columns from `y` to `x`, matching rows based on the keys:

    - `inner`: includes all rows in `x` and `y`.
    - `left`: includes all rows in `x`.
    - `right`: includes all rows in `y`.
    - `outer`: includes all rows in `x` or `y`.

    If a row in `x` matches multiple rows in `y`, all the rows in `y` will be returned once for
    each matching row in `x`.

    Parameters:

    - `y`: DataFrame or Recipe to join with.
    - `how`: Type of the join: `left`, `right`, `inner` or `full`
    - `by`: optional colum name list to join by. Default: `None`
    - `df`: optional df to be used as input if `y` is a Recipe
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Inner Join with another DataFrame
    # `sales_df` and `client_df` are DataFrames, `by` argument is optional
    Recipe([
        JoinStep(sales_df, how="inner", by="client_id")
    ]).bake(client_df)

    # Inner join with the DataFrame obtained from the execution of a Recipe
    # sales_recipe will be executed using sales_df inside the client_recipe execution
    sales_recipe = Recipe([
        RenameStep({'client_id': 'cid'})
    ])

    client_recipe = Recipe([
        JoinStep(sales_recipe, how="inner", by=["client_id", "region_id"], df=sales_df)
    ])

    client_recipe.prepare(client_df).bake(client_df)
    ```

    Raises:

    - `YeastValidationError`: if any of the validations is not correct.
    """
    how_types = ['left', 'right', 'inner', 'full', 'outer']

    def __init__(self, y, how="left", by=None, df=None, role='all'):
        self.y = y
        self.how = 'outer' if how == 'full' else how
        self.by = by if not by else by if type(by) in [list, tuple] else [by]
        self.df = df
        super().__init__(needs_preparation=False, role=role)

    def do_prepare(self, left):
        # Prepare the Recipe before Merges
        if isinstance(self.y, Recipe):
            self.y = self.y.prepare(self.df)

    def do_bake(self, left):
        if isinstance(self.y, Recipe):
            self.y = self.y.bake(self.df)
        return left.merge(self.y, how=self.how, on=self.by, suffixes=['_x', '_y'])

    def do_validate(self, x):
        """
        - How must be a valid type
        - We are expecting DataFrame or Recipe on Right
        - Left must be a DataFrame
        - All columns in by must be on Left
        - All columns in by must be on Right
        - df is only supported if right is a Recipe
        """
        # Validate How parameter
        if self.how not in self.how_types:
            raise YeastValidationError(f'Join type "{self.how}" not between: {self.how_types}')
        # We are expecting DataFrame or Recipe on Right
        if not isinstance(self.y, DataFrame) and not isinstance(self.y, Recipe):
            raise YeastValidationError('We are expecting a DataFrame or a Recipe or Right')
        # Left must be a DataFrame
        if not isinstance(x, DataFrame):
            raise YeastValidationError("Previous Step didn't return a DataFrame")
        # All columns in by must be on Left
        if self.by:
            missing = [c for c in self.by if c not in x.columns]
            if missing:
                raise YeastValidationError(
                    f"Columns {missing} not found on the x side of the merge"
                )
        # All columns in by must be on Right
        if self.by and isinstance(self.y, DataFrame):
            missing = [c for c in self.by if c not in self.y.columns]
            if missing:
                raise YeastValidationError(
                    f"Columns {missing} not found on the right side of the merge"
                )
        # self.df is only supported if right is a Recipe
        if self.df is not None and not isinstance(self.y, Recipe):
            raise YeastValidationError(f"'df' parameter is only supported if right is a Recipe")
