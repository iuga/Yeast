# Methods for Groups and Aggregations

Most data operations are done on groups defined by columns. `GroupByStep` takes an existing DataFrame and converts it into a Pandas `DataFrameGroupBy` where aggregation/summarization/mutation operations are performed "by group".

A group by operation involves some combination of:

- Splitting the object: `GroupByStep()`
- Applying functions: `SummarizeStep()` or `MutateStep()`
- And combining the results into a DataFrame.

## Summarizations / Aggregations

In order to create one or more numeric variables summarizing the columns of an existing group created by `GroupByStep()` you need to use `SummarizeStep()` that will result in one row in the output for each group.

On a simple example:

```python
recipe = Recipe([
    # Group the data by client_id and branch columns
    GroupByStep(['client_id', 'branch_id']),
    # Let's summarize the data:
    SummarizeStep({
      # The total sales are the sum of the ticket_total
      'total_sales': AggSum('ticket_total'),
      # Number of sales to the client in that branch
      'number_of_sales': AggCount('ticket_id')
    })
])
```
```bash
   client_id  branch_id  total_sales  number_of_sales  
0       2121        3AX       3453.4               12
1       2122        3AX          202                2
1       1034        4BA        25345               42
```

The most common aggregations are:

- ::: yeast.aggregations.AggMean
    :docstring:
- ::: yeast.aggregations.AggMedian
    :docstring:
- ::: yeast.aggregations.AggMax
    :docstring:
- ::: yeast.aggregations.AggMin
    :docstring:
- ::: yeast.aggregations.AggCount
    :docstring:
- ::: yeast.aggregations.AggCountDistinct
    :docstring:

## What's next?

[Available Steps](reference.md)
