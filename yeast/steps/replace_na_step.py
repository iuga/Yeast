from yeast.step import Step
from yeast.errors import YeastValidationError


class ReplaceNAStep(Step):
    """
    Replace missing values

    Parameters:

    - `mapping`: replacing mapping as `{'column': replacement_value, ...}` or string column name.
    - `value`: value to replace the NAs if mapping is a string column name. Default: `0`

    Usage:

    ```python
    # Replace NA values in one column
    ReplaceNAStep('factor', 1.0)

    # Replace NA values on several columns
    ReplaceNAStep({
        'factor': 1.00,
        'pending': 0.00,
        'category': 'other'
    })
    ```

    Raises:

    - `YeastValidationError`: if a column does not exist on the dataframe
    """
    def __init__(self, mapping, value=0):
        self.mapping = mapping
        self.value = value

    def do_bake(self, df):
        if isinstance(self.mapping, str):
            self.mapping = {self.mapping: self.value}
        for column, value in self.mapping.items():
            df[column] = df[column].fillna(value)
        return df

    def do_validate(self, df):
        """
        - Mapping must be a string or a dict
        - All columns on the mapping must exist on the df
        """
        if type(self.mapping) not in [dict, str]:
            raise YeastValidationError(f'The replacement mapping must be a string or dict')
        if isinstance(self.mapping, dict):
            matches = [c in df.columns for c in self.mapping.keys()]
            if not all(matches):
                missing_columns = [c for c, v in zip(self.mapping.keys(), matches) if not v]
                raise YeastValidationError(f'The following columns are missing: {missing_columns}')
        if isinstance(self.mapping, str) and self.mapping not in df.columns:
            raise YeastValidationError(f'The following column is missing: {self.mapping}')
