from yeast.step import Step
from yeast.selectors import AllColumns


class DropZVColumnsStep(Step):
    """
    Drop all columns that contain only a single value (Zero Variance).

    Notes:

    The parameter `naomit` is used to indicate if `NA` should be considered as a value.
    If `naomit=False` then `[NA, 'a']` will contain two values and it will not be removed.
    If `naomit=True` then `[NA, 'a']` will contain only one value and will be filtered because `NA`
    was not considered.

    Parameters:

    - `selector`: string list of column names or a selector to impute.
    - `naomit`: True if NA is not considered a value, False otherwise.
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Remove all columns that contains zero variance:
    recipe = Recipe([
        DropZVColumnsStep()
    ])

    # Remove all numerical columns that contains zero variance:
    recipe = Recipe([
        DropZVColumnsStep(AllNumeric())
    ])
    ```
    """
    def __init__(self, selector=None, naomit=False, role='all'):
        self.selector = selector if selector else AllColumns()
        self.naomit = naomit
        super().__init__(needs_preparation=True, role=role)

    def do_prepare(self, df):
        columns = self.resolve_selector(self.selector, df)
        summary = df[columns].nunique(dropna=self.naomit)
        self.removals = summary[summary == 1].index.tolist()

    def do_bake(self, df):
        return df.drop(columns=self.removals)
