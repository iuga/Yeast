from yeast.step import Step
from yeast.errors import YeastValidationError


class MeanImputeStep(Step):
    """
    Impute numeric data using the mean

    MeanImputeStep estimates the variable mean from the prepare data then applies the new values
    to new data sets using these averages.

    Parameters:

    - `selector`: string list of column names or a selector to impute
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Impute the age and size column using the mean from the training set
    MeanImputeStep(['age', 'size'])

    # You can also use selectors:
    MeanImputeStep(AllNumeric())
    ```

    Raises:

    - `YeastValidationError`: if a column does not exist
    """
    def __init__(self, selector, role='all'):
        self.selector = selector
        self.means = {}
        super().__init__(needs_preparation=True, role=role)

    def do_prepare(self, df):
        """
        Calculate the column means on the prepare dataset
        """
        columns = self.resolve_selector(self.selector, df)
        for column in columns:
            self.means[column] = df[column].mean(skipna=True)

    def do_bake(self, df):
        """
        Replace all NA values with the calculated means
        """
        columns = self.resolve_selector(self.selector, df)
        for column in columns:
            df[column] = df[column].fillna(self.means[column])
        return df

    def do_validate(self, df):
        """
        - All columns on the mapping must exist on the df
        """
        columns = self.resolve_selector(self.selector, df)

        matches = [c in df.columns for c in columns]
        if not all(matches):
            missing_columns = [c for c, v in zip(columns, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')
