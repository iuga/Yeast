from yeast.step import Step
from yeast.errors import YeastValidationError, YeastPreparationError


class MeanImputeStep(Step):
    """
    Impute numeric data using the mean

    MeanImputeStep estimates the variable mean from the prepare data then replace the NA values
    on new data sets using the calculated mean values.

    Parameters:

    - `selector`: string list of column names or a selector to impute
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Impute the age and size columns using the mean from the training set
    # Age :  20,  31,  65,  NA,  45,  23,  NA
    # Size:   2,   5,   9,   3,   4,  NA,  NA
    # to
    # Age :  20,  31,  65, 36.8, 45,  23, 36.8 (mean=36.8)
    # Size:   2,   5,   9,    3,  4, 4.6,  4.6 (mean=4.6)
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
            try:
                self.means[column] = df[column].mean(skipna=True)
            except TypeError as ex:
                raise YeastPreparationError(f'Error calculating the mean on: {column}') from ex

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
