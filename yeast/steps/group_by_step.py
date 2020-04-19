from yeast.step import Step
from yeast.errors import YeastValidationError


class GroupByStep(Step):
    """
    Most data operations are done on groups defined by columns.
    GroupByStep takes an existing DataFrame and converts it into a Pandas DataFrameGroupBy where
    aggregation/summarization/mutation operations are performed "by group".

    A groupby operation involves some combination of:
    - Splitting the object: `GroupByStep()`
    - Applying functions: `SummarizeStep()` or `MutateStep()`
    - And combining the results into a DataFrame.

    Parameters:

    - `columns`: list of string column names to group by or a selector

    Usage:

    ```python
    # Basic Group By and an Aggregation
    recipe = Recipe([
        GroupByStep(['category', 'year']),
        SummarizeStep({
            'average_rating': AggMean('rating'),
            'unique_titles': AggCountDistinct('title')
        })
    ])
    ```

    Raises:

    - `YeastValidationError`: if a column does not exist on the DataFrame
    """
    def __init__(self, columns):
        self.selector = columns
        super().__init__()

    def do_bake(self, df):
        return df.groupby(self.selector, sort=True)

    def do_validate(self, df):
        """
        - Check if the df contains all listed columns
        """
        self.selector = self.resolve_selector(self.selector, df)

        matches = [c in df.columns for c in self.selector]
        if not all(matches):
            missing_columns = [c for c, v in zip(self.selector, matches) if not v]
            raise YeastValidationError(f'The following columns are missing: {missing_columns}')
