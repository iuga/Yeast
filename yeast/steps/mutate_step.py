from types import LambdaType
from yeast.step import Step
from yeast.errors import YeastBakeError
from yeast.transformers import Transformer


class MutateStep(Step):
    """
    Create or transform variables mantaining the number of rows appliyng a list of transformers.
    If more than one transformer is passed to a column, they will be executed in order.
    New variables overwrite existing variables of the same name.

    Parameters:

    - `transformers`: Dictionary of transformers using keys as column names and values as
                      transformers. E.g: `{ column_name: Transformer }`.
                      It also support lambda functions. E.g: `{var : lambda df: df}` and a
                      list of transforers (lambda or Transformer: `{var: [tx1, tx2, ...]}`

    Short-Term Roadmap:

    - Using custom functions
    - Using mutate after `GroupByStep()`
    - If column is not defined, use the destination column

    Usage:

    ```python
    # Create a variable using a lambda function
    Recipe([
        MutateStep({
            'total_sales': lambda df: df.sales + df.fee
        })
    ])

    # Create or update variables using Transformers
    Recipe([
        MutateStep({
            "name": StrToLower('name'),
            "uid: : StrToUpper('uid')
        })
    ])

    # Create or update variables using mutiple Transformers
    # You can use Transformers or Lambda functions
    Recipe([
        MutateStep({
            "name": [
                StrReplace('-1', ''),
                StrToTitle('name')
            ]
        })
    ])

    # Create or update variables using Group Transformers
    Recipe([
        # Create or update a variable
        GroupByStep('client_id'),
        MutateStep({
            "row_number": RowNumber(),
            "lag_sales": NumericLag('sales'),
            "lead_sales": NumericLead('sales')
        })
    ])

    # Create or update a variable using a custom function
    def new_variable(x):
        return x.sales / 1e6

    Recipe([
        # Create or update a variable
        MutateStep({
            'mean_sales': new_variable,
        })
    ])
    ```

    Raises:

    - `YeastValidationError`: xxx
    """
    def __init__(self, transformers):
        self.transformers = transformers

    def do_bake(self, df):
        for column, transformers in self.transformers.items():
            transformers = transformers if type(transformers) in [list, tuple] else [transformers]
            for transformer in transformers:
                if isinstance(transformer, LambdaType):
                    df = self.assign_lamda(df, column, transformer)
                if isinstance(transformer, Transformer):
                    df = self.assign_transformer(df, column, transformer)
        return df

    def assign_lamda(self, df, column, tx):
        """
        Create or update a column using a lambda function
        """
        try:
            df[column] = tx(df)
            return df
        except KeyError as ex:
            raise YeastBakeError(f'There was an error on the lambda function: {type(ex)} {ex}')

    def assign_transformer(self, df, column, tx):
        """
        Create or update a column using a transformer

        desc = StrToLower()
        df['desc'] = step.resolve(df['desc'])

        lower_desc = StrToLower('desc')
        df['lower_desc'] = step.resolve(df['desc'])
        """
        try:
            df[column] = tx.resolve(df)
            return df
        except KeyError as ex:
            raise YeastBakeError(f'There was an error on the lambda function: {type(ex)} {ex}')

    def do_validate(self, df):
        """
        - All keys should be string
        - All values should be callables or transformers
        """
        pass
