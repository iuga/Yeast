from yeast.step import Step
from yeast.errors import YeastValidationError


class RenameColumnsStep(Step):
    """
    Step in charge of renaming columns based on a mapping dictionary.
    Columns that don't exist are ignored.

    Parameters:

    - `mapping`: rename mapping as { 'old_name': 'new_name', ... }
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    RenameColumnsStep({
        'old_column_name': 'new_column_name'
    })
    ```

    Raises:

    - `YeastValidationError`: if any column old or new is not a string.
    """
    def __init__(self, mapping, role='all'):
        self.mapping = mapping
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        return df.rename(columns=self.mapping)

    def do_validate(self, df):
        """
        Validations:
        - Check that all columns names (old and new) are not empty strings
        """
        for c in self.mapping.keys():
            if not isinstance(c, str) or c.strip == '':
                raise YeastValidationError(f'New column name "{c}" should be a non empty string')
        for c in self.mapping.values():
            if not isinstance(c, str) or c.strip == '':
                raise YeastValidationError(f'Old column name "{c}" should be a non empty string')
