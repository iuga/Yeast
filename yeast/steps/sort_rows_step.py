from yeast.step import Step
from yeast.errors import YeastValidationError


class SortRowsStep(Step):
    """
    Step in charge of sorting rows based on columns.

    Parameters:

    - `columns`: list of string column names to sort by
    - `ascending`: boolean flag wo sort ascending vs. descending
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    SortRowsStep(['B', 'C'])
    ```

    Raises:

    - `YeastValidationError`: if any column does not exist or any column name is invalid.
    """
    def __init__(self, columns, ascending=True, role='all'):
        self.selector = columns
        self.ascending = ascending if isinstance(ascending, bool) else True
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        return df.sort_values(by=self.selector, axis=0, ascending=self.ascending, ignore_index=True)

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


class SortStep(SortRowsStep):
    """
    SortStep is an Alias for SortRowsStep
    """
    pass
