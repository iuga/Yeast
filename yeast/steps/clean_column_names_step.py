from yeast.step import Step
from yeast.errors import YeastValidationError
from inflection import underscore, camelize


class CleanColumnNamesStep(Step):
    """
    Step in charge of clean all columns names.

    Available cases:

    - `snake` from `column Name` to `column_name`
    - `lower_camel` from `column Name` to `columnName`
    - `upper_camel` from `column Name` to `ColumnName`

    Parameters:

    - `case`: case that will be used on the columns, `snake` by default.
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # DataFrame columns: ['TheName', 'B', 'the name', 'Other Name']
    CleanColumnNamesStep('snake')
    # DataFrame result columns: ['the_name', 'b', 'the_name', 'other_name']
    ```

    Raises:

    - `YeastValidationError`: if the case is not available.
    """
    cases = ['snake', 'lower_camel', 'upper_camel']

    def __init__(self, case="snake", role='all'):
        self.case = case
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        if self.case == 'snake':
            mapper = {
                c: underscore(c.strip().replace('  ', ' ').replace(' ', '_')) for c in df.columns
            }
        elif self.case in ['upper_camel', 'lower_camel']:
            upper = bool(self.case == 'upper_camel')
            mapper = {
                c: camelize(
                    c.strip().replace('  ', ' ').replace(' ', ''),
                    uppercase_first_letter=upper
                ) for c in df.columns
            }
        return df.rename(columns=mapper)

    def do_validate(self, df):
        """
        Validations:
        - Format is available
        """
        if self.case not in self.cases:
            raise YeastValidationError(f'Invalid format names. Choose between: {self.cases}')
