from yeast.step import Step
from yeast.errors import YeastValidationError


class ConstantImputeStep(Step):
    """
    Impute data using a constant value

    ConstantImputeStep replaces all NA values in the columns by a constant value. This step does not
    validate the column data type before impute, so you can generate mixed types on a column.

    Parameters:

    - `selector`: string list of column names or a selector to impute
    - `value`: constant value to replace with
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Numerical:
    # Impute the age and size columns using zero as value
    # Age :  20,  31,  65,  NA,  45,  23,  NA
    # Size:   2,   5,   9,   3,   4,  NA,  NA
    # to
    # Age :  20,  31,  65,   0,  45,  23,   0
    # Size:   2,   5,   9,   3,   4,   0,   0
    ConstantImputeStep(['age', 'size'], value=0)

    # Categorical:
    # Impute the security column with "other"
    # security: 'stock', 'bond', 'etf', 'mf', NA
    # to
    # security: 'stock', 'bond', 'etf', 'mf', 'other'
    ConstantImputeStep(['security'], value='other')

    # You can also use selectors:
    ConstantImputeStep(AllNumeric(), value=0)
    ```

    Raises:

    - `YeastValidationError`: if a column does not exist
    """
    def __init__(self, selector, value, role='all'):
        self.selector = selector
        self.value = value
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        """
        Replace all NA values with the constant value
        """
        columns = self.resolve_selector(self.selector, df)
        for column in columns:
            df[column] = df[column].fillna(self.value)
        return df

    def do_validate(self, df):
        """
        - All columns on the mapping must exist on the df
        """
        columns = self.resolve_selector(self.selector, df)

        matches = [c in df.columns for c in columns]
        if not all(matches):
            missing_columns = [c for c, v in zip(columns, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')
