from yeast.step import Step
from yeast.errors import YeastValidationError, YeastPreparationError


class MedianImputeStep(Step):
    """
    Impute numeric data using the median

    MedianImputeStep estimates the variable median from the prepare data then replace the NA values
    on new data sets using the calculated median values.

    Parameters:

    - `selector`: string list of column names or a selector to impute
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Impute the age and size columns using the mean from the training set
    # Age :  20,  31,  65,  NA,  45,  23,  NA
    # Size:   2,   5,   9,   3,   4,  NA,  NA
    # to
    # Age :  20,  31,  65,  31,  45,  23,  31 (median=31)
    # Size:   2,   5,   9,   3,   4,   4,   4 (median=4)
    MedianImputeStep(['age', 'size'])

    # You can also use selectors:
    MedianImputeStep(AllNumeric())
    ```

    Raises:

    - `YeastValidationError`: if a column does not exist
    """
    def __init__(self, selector, role='all'):
        self.selector = selector
        self.medians = {}
        super().__init__(needs_preparation=True, role=role)

    def do_prepare(self, df):
        """
        Calculate the column medians on the prepare dataset
        """
        columns = self.resolve_selector(self.selector, df)
        for column in columns:
            try:
                self.medians[column] = df[column].median(skipna=True)
            except TypeError as ex:
                raise YeastPreparationError(f'Error calculating the median on: {column}') from ex

    def do_bake(self, df):
        """
        Replace all NA values with the calculated medians
        """
        columns = self.resolve_selector(self.selector, df)
        for column in columns:
            df[column] = df[column].fillna(self.medians[column])
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
