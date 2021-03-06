from yeast.step import Step
from yeast.errors import YeastValidationError


class DropDuplicateRowsStep(Step):
    """
    Step in charge of remove duplicate rows, optionally only considering certain columns.

    Parameters:

    - `columns`: list of string column names to look for duplicates or a selector
    - `keep` (`first, last, none`): Determines which duplicates (if any) to keep. `first` : Drop
                                    duplicates except for the first occurrence. `last` : Drop
                                    duplicates except for the last occurrence. `none` : Drop
                                    all duplicates.
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Remove duplicates considering all columns, keep the first occurence
    DropDuplicatesStep()

    # Remove duplicates considering columnc B and C
    DropDuplicatesStep(['B', 'C'], keep="none")

    # Removing duplicates considering all columns starting with id_
    DropDuplicatesStep(AllMatching('^id_'), keep="first")
    ```

    Raises:

    - `YeastValidationError`: if any column does not exist or any column name is invalid.
    """
    def __init__(self, columns=None, keep="first", role='all'):
        self.selector = columns
        self.keep = {
            'first': 'first',
            'last': 'last',
            'none': False
        }.get(keep, 'first')
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        return df.drop_duplicates(subset=self.selector, keep=self.keep)

    def do_validate(self, df):
        """
        - Check that all columns are not empty strings
        - Check if the df contains all elements in columns
        """
        # If None, pick all columns
        self.selector = df.columns if self.selector is None else self.selector

        self.selector = self.resolve_selector(self.selector, df)

        if not all(isinstance(c, str) for c in self.selector):
            raise YeastValidationError('Invalid column names')

        matches = [c in df.columns for c in self.selector]
        if not all(matches):
            missing_columns = [c for c, v in zip(self.selector, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')


class DropDuplicatesStep(DropDuplicateRowsStep):
    """
    DropDuplicatesStep is an Alias for DropDuplicateRowsStep
    """
    pass
