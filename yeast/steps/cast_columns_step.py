from yeast.step import Step
from yeast.errors import YeastValidationError


class CastColumnsStep(Step):
    """
    Step in charge of casting columns to a type based on a mapping dictionary.

    Available Types:

    - `category`
    - `string`, `str`
    - `boolean`, `bool`
    - `integer`, `int64`, `int32`
    - `float`, `float64`, `float32`
    - `date`, `datetime`, `datetime64`

    Parameters:

    - `mapping`: Casting mapping as { 'column_name': 'type', ... }
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    CastColumnsStep({
        'title': 'string',
        'year': 'integer',
        'aired': 'datetime',
    })
    ```

    Raises:

    - `YeastValidationError`: if any column or type is not correct.
    """
    type_mapper = {
        'string': 'string',
        'boolean': 'boolean',
        'integer': 'int64',
        'float': 'float64',
        'str': 'string',
        'bool': 'boolean',
        'datetime64': 'datetime64',
        'datetime': 'datetime64',
        'date': 'datetime64',
        'category': 'category',
        'float64': 'float64',
        'int64': 'int64',
        'int32': 'int32',
        'float32': 'float32'
    }

    def __init__(self, mapping, role='all'):
        self.mapping = mapping
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        return df.astype(self.convert_mapping(self.mapping))

    def convert_mapping(self, mapping):
        pandas_mapping = {}
        for c, t in mapping.items():
            pandas_mapping[c] = self.type_mapper.get(t, 'object')
        return pandas_mapping

    def do_validate(self, df):
        """
        Validations:
        - Columns must exist
        - Types must exist
        """
        for c, t in self.mapping.items():
            if c not in df.columns:
                raise YeastValidationError(f'Column {c} not found on the DataFrame')
            if t not in self.type_mapper.keys():
                raise YeastValidationError(
                    f'Data type {t} not available. Choose from: {self.type_mapper.keys()}'
                )


class CastStep(CastColumnsStep):
    """
    CastStep is an Alias for CastColumnsStep
    """
    pass
