
## Short-term roadmap:

**Row and Column Operations**

- `MutateStep`
- `DropZVColumnsStep`
- `ReplaceNAStep`
- `LagStep` and `LeadStep`
- `PivotLongerStep` and `PivotWiderStep`

**Individual Transformations**

- `ColumnMapValuesStep`
- `ColumnStringReplaceStep`
- `ReplaceNAStep`
- `IfElseStep`

**Documentation Steps**

- `DescribeStep`

**Validation Steps**

- `CheckColumnsStep`
- `CheckSameLength` for Merge Operations

**Transformers**

- `NumericRound(x, digits=1)`
- `Rank(ties_method = {‘average’, ‘min’, ‘max’, ‘first’, ‘dense’})`
- `RowNumber()` : Equivalent to Rank(ties.method = "first")
- `RankFirst()`: Equivalent to rank(ties.method = "min")
- `RankMin()`: Equivalent to rank(ties.method = "min")
- `RankMax()`: Equivalent to rank(ties.method = "max")
- `RankDense()`: Like MinRank(), but with no gaps between ranks
- `RankPercent()`: a number between 0 and 1 computed by rescaling min_rank to [0, 1]
- `XXXLag()`
- `XXXLead()`

**Aggregations**

-

**Selectors**

- Enhance the documentation, same structure than transformers

**Workflows**

- `LeftJoinStep`
- `InnerJoinStep`
- `RightJoinStep`
- `FullJoinStep`
- Concatenate, Merge and Join Difference Recipes

**Library**

- Define the * exports

**Documentation**

- Prepare a Python Notebook with an end to end read example
- Improve CSS on the docstrings

**Bugs**
