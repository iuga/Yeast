from yeast.step import Step
from yeast.errors import YeastValidationError


class SelectColumnStep(Step):
    """
    Step in charge of keep columns based on their names.

    Parameters:

    - `columns`: list of string column names to keep

    Usage:

    ```python
    # DataFrame columns: ['A', 'B', 'C', 'D']
    SelectColumnStep(['B', 'C'])
    # DataFrame result columns: ['B', 'C']
    ```

    Raises:

    - `YeastValidationError`: if any column does not exist or any column name is invalid.
    """
    def __init__(self, columns):
        self.columns = columns
        super().__init__()

    def do_bake(self, df):
        return df[self.columns]

    def do_validate(self, df):
        """
        Validations:
        - Check that all columns are not empty strings
        - Check if the df contains all elements in columns
        """
        if not all(isinstance(c, str) for c in self.columns):
            raise YeastValidationError('Invalid column names')

        matches = [c in df.columns for c in self.columns]
        if not all(matches):
            missing_columns = [c for c, v in zip(self.columns, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')
