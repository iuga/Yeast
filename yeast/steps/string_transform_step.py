from yeast.step import Step
from yeast.errors import YeastValidationError
from yeast.transformers import StrTransformer


class StringTransformStep(Step):
    """
    Step in charge of transform a String column using a list of String transformers.
    All transformers will be applied in order.

    Parameters:

    - `columns`: list of string column names to look for duplicates or a selector
    - `transformers`: list of String transformers

    Usage:

    ```python
    # Define a recipe of steps to process your data
    recipe = Recipe([
      # The "user_id" column (string) need some cleaning
      # Example "  3a2-A " must match with "0003A2"
      StringTransformStep(columns=['user_id'], transformers=[
        # Remove whitespaces from start and end of string
        StrTrim(),
        # The prefix "-A" should be removed
        StrReplace('-A', ''),
        # Transform to uppercase
        StrToUpper(),
        # Pad the left side with zeros
        StrPad(width=6, side='left', pad='0')
      ])
    ])
    ```

    Raises:

    - `YeastValidationError`: If the column does not exist or there is an error on the transformers
    """
    def __init__(self, columns, transformers):
        self.selector = columns
        self.transformers = transformers
        super().__init__()

    def do_bake(self, df):
        for column_name in self.selector:
            for transformer in self.transformers:
                df[column_name] = transformer.resolve(df[column_name])
        return df

    def do_validate(self, df):
        """
        - Check that all columns are not empty strings
        - Check if the df contains all elements in columns
        - Check that all transformers inherit from StrTransformer
        """
        self.selector = self.resolve_selector(self.selector, df)

        if not all(isinstance(c, str) for c in self.selector):
            raise YeastValidationError('Invalid column names')

        matches = [c in df.columns for c in self.selector]
        if not all(matches):
            missing_columns = [c for c, v in zip(self.selector, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')

        for transformer in self.transformers:
            if not isinstance(transformer, StrTransformer):
                raise YeastValidationError(f'Transformer {transformer} not recognized')
