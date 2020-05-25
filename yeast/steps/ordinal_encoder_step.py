import pandas as pd
from yeast.step import Step
from yeast.errors import YeastValidationError


class OrdinalEncoderStep(Step):
    """
    Encode categorical/string discrete features as integer numbers (0 to n - 1).

    Parameters:

    - `selector`: List of columns, column name or selector.
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    recipe([
        # Ordinal Encode the gender column
        OrdinalEncoderStep('gender')
    ])

    # Extract the categories and the values on the prepare
    recipe = recipe.prepare(train_data)

    # Encode on new data without changing the values
    test_data = recipe.bake(test_data)

    # Example:
    # Gender: 'Male', 'Female', 'Male', None, 'Male', 'Female'
    # Encoded: 0, 1, 0, NA, 0, 1
    ```

    Raises:

    - `YeastValidationError`: If the column was not found
    """
    def __init__(self, selector, role='all'):
        self.selector = selector
        self.mappings = {}
        super().__init__(needs_preparation=True, role=role)

    def do_prepare(self, df):
        """
        Map each unique value in the column into a integer.
        NA and None values are ignored and remain the same.
        """
        columns = self.resolve_selector(self.selector, df)
        for column in columns:
            categories = df[column].sort_values().unique().tolist()
            self.mappings[column] = {
                category: ordinal for ordinal, category in enumerate(categories)
                if not pd.isna(category)
            }

    def do_bake(self, df):
        """
        Map the values from the discrete categorical column to nullable integers.
        """
        columns = self.resolve_selector(self.selector, df)
        for column in columns:
            df[column] = df[column].replace(self.mappings[column]).astype('Int32')
            df[column] = df[column].where(df[column].notnull(), None)
        return df

    def do_validate(self, df):
        """
        - Column must exist
        """
        columns = self.resolve_selector(self.selector, df)

        matches = [c in df.columns for c in columns]
        if not all(matches):
            missing_columns = [c for c, v in zip(columns, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')
