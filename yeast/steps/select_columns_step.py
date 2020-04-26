from yeast.step import Step
from yeast.errors import YeastValidationError


class SelectColumnsStep(Step):
    """
    Step in charge of keep columns based on their names or selectors

    Parameters:

    - `columns`: list of string column names, selectors or combinations to keep

    Usage:

    ```python
    # ['A', 'B', 'C', 'D']
    SelectColumnsStep('B')
    # ['B']

    # ['A', 'B', 'C', 'D']
    SelectColumnsStep(['B', 'C'])
    # ['B', 'C']

    # ['A', 'B', 'C', 'D']
    SelectColumnsStep(AllNumeric())
    # ['B']

    # ['AA', 'AB', 'C', 'D']
    SelectColumnsStep([AllMatching('^A'), 'D'])
    # ['AA', 'AB', 'D']
    ```

    Raises:

    - `YeastValidationError`: if any column does not exist or any column name is invalid.
    """
    def __init__(self, columns):
        self.selector = columns
        super().__init__()

    def do_bake(self, df):
        return df[self.selector]

    def do_validate(self, df):
        """
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


class SelectStep(SelectColumnsStep):
    """
    SelectStep is an Alias for SelectColumnsStep
    """
    pass
