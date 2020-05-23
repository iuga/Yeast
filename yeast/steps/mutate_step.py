from types import LambdaType
from pandas.core.groupby.generic import DataFrameGroupBy
from yeast.step import Step
from yeast.errors import YeastBakeError, YeastValidationError
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
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

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
            "uid": : StrToUpper('uid')
        })
    ])

    # If the output column is the same as the input column you don't need to
    # set the column name. The result will be the same
    Recipe([
        MutateStep({
            "name": StrToLower(),  # name will be transformed to lower case
            "uid": : StrToUpper()   # uid will be transformed to upper case
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
    def new_variable(df):
        return df.sales / 1e6

    Recipe([
        MutateStep({
            'mean_sales': new_variable,
        })
    ])
    ```

    Raises:

    - `YeastBakeError`: If there was an error executing any transformer
    - `YeastValidationError`: xxx
    """
    def __init__(self, transformers, role='all'):
        self.transformers = transformers
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        for column, transformers in self.transformers.items():
            transformers = transformers if type(transformers) in [list, tuple] else [transformers]
            for transformer in transformers:
                df = self.assign_transformer(df, column, transformer)
        return df

    def assign_transformer(self, df, column, transformer):
        """
        Create or update a column using a lambda function
        """
        try:
            # Set the column name if empty, using the destination column
            if isinstance(transformer, Transformer):
                transformer.set_column_if_required(column)
            # Split between groups and dataframes
            if isinstance(df, DataFrameGroupBy):
                df = df.apply(self.add_column, column=column, values=transformer(df))
            else:
                df[column] = transformer(df)
            return df
        except KeyError as ex:
            raise YeastBakeError(
                f'There was an error executing the transformer: {transformer} on {column}'
            ) from ex

    @staticmethod
    def add_column(df, column, values):
        """
        Static methof to add a column using apply. Usually for Groups:
        """
        df[column] = values
        return df

    def do_validate(self, df):
        """
        - All keys should be valid column names
        - All values should be callables or transformers or list of those things
        """
        for column in self.transformers.keys():
            if not isinstance(column, str) and column.strip() == '':
                raise YeastValidationError(f'"{column}" is not a valid column name')
        for item in self.transformers.values():
            if type(item) in [list, tuple]:
                for subitem in item:
                    if not isinstance(subitem, Transformer) and not isinstance(subitem, LambdaType):
                        raise YeastValidationError(f"Transformer {subitem} not recognized")
            else:
                if not isinstance(item, Transformer) and not isinstance(item, LambdaType):
                    raise YeastValidationError(f"Transformer {item} not recognized")
