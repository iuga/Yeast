from yeast.steps.join_step import JoinStep


class FullJoinStep(JoinStep):
    """
    Full Join two DataFrames together

    Return all rows and all columns from both `x` and `y`.
    Where there are not matching values, returns `NA` for the one missing.

    Parameters:

    - `y`: DataFrame or Recipe to merge with.
    - `by`: optional colum name list to merge by. Default: `None`
    - `df`: optional df to be used as input if `y` is a Recipe

    Usage:

    ```python
    # Full Outer Join with another DataFrame
    # sales_df and client_df are DataFrames, by argument is optional
    Recipe([
        FullJoinStep(sales_df, by="client_id")
    ]).bake(client_df)

    # Full Outer join with the DataFrame obtained from the execution of a Recipe
    # sales_recipe will be executed using sales_df inside the client_recipe execution
    sales_recipe = Recipe([
        RenameStep({'client_id': 'cid'})
    ])

    client_recipe = Recipe([
        FullJoinStep(sales_recipe, by=["client_id", "region_id"], df=sales_df)
    ])

    client_recipe.prepare(client_df).bake(client_df)
    ```

    Raises:

    - `YeastValidationError`: if any of the validations is not correct.
    """
    def __init__(self, y, by=None, df=None):
        self.y = y
        self.how = "outer"
        self.by = by if not by else by if type(by) in [list, tuple] else [by]
        self.df = df
