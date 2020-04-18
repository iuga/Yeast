from yeast.step import Step
from yeast.errors import YeastValidationError


class DropColumnsStep(Step):
    """
    Step in charge of drop columns based on their names.

    Parameters:

    - `columns`: list of string column names to drop or a selector.

    Usage:

    ```python
    # DataFrame columns: ['A', 'B', 'C', 'D']
    DropColumnsStep(['B', 'C'])
    # DataFrame result columns: ['A', 'D']
    ```

    Raises:

    - `YeastValidationError`: if any column does not exist or any column name is invalid.
    """
    def __init__(self, columns):
        self.selector = columns
        super().__init__()

    def do_bake(self, df):
        return df.drop(columns=self.selector)

    def do_validate(self, df):
        """
        Validations:
        - Check that all columns are not empty strings
        - Check if the df contains all elements in columns
        """
        self.selector = self.resolve_selector(self.selector, df)

        if not all(isinstance(c, str) for c in self.selector):
            raise YeastValidationError('Invalid column names')

        matches = [c in df.columns for c in self.selector]
        if not all(matches):
            missing_columns = [c for c, v in zip(self.selector, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')
