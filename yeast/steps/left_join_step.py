from yeast.steps.join_step import JoinStep


class LeftJoinStep(JoinStep):
    """
    Left Join two DataFrames together

    Return all rows from `x`, and all columns from `x` and `y`.
    Rows in `x` with no match in `y` will have NA values in the new columns.
    If there are multiple matches between `x` and `y` all combinations of the matches
    are returned.

    Parameters:

    - `y`: DataFrame or Recipe to merge with.
    - `by`: optional colum name list to merge by. Default: `None`
    - `df`: optional df to be used as input if `y` is a Recipe
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

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
    def __init__(self, y, by=None, df=None, role='all'):
        super().__init__(
            y,
            how="left",
            by=by if not by else by if isinstance(by, (list, tuple)) else [by],
            df=df,
            role=role
        )
