from pandas.core.groupby.generic import DataFrameGroupBy

from yeast.step import Step
from yeast.errors import YeastValidationError


class SummarizeStep(Step):
    """
    Create one or more numeric variables summarizing the columns of an existing group created by
    GroupByStep() resulting in one row in the output for each group. Please refer to the
    Aggregations documentation to see the complete list of supported aggregations.
    The most used ones are: `AggMean`, `AggMedian`, `AggCount`, `AggMax`, `AggMin`

    Parameters:

    - `aggregations`: dictionary with the aggregations to perform. The key is the new column name
                      where the value is the specification of the aggregation to perform.
                      For example: `{'new_column_name': AggMean('column')}`
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Basic Summarization on a Group
    recipe = Recipe([
        GroupByStep(['category', 'year']),
        SummarizeStep({
            'average_rating': AggMean('rating'),
            'unique_titles': AggCountDistinct('title')
        })
    ])
    ```

    Raises:

    - `YeastValidationError`: If there was not a GroupByStep before
    """
    def __init__(self, aggregations, role='all'):
        self.aggregations = aggregations
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, gdf):
        aggs = {}
        for column, agg in self.aggregations.items():
            aggs[column] = agg.resolve(gdf)
        return gdf.agg(**aggs).reset_index()

    def do_validate(self, gdf):
        """
        - A GroupByStep was applied before this step
        """
        if not isinstance(gdf, DataFrameGroupBy):
            raise YeastValidationError('This step must be executed after a GroupByStep(...)')
