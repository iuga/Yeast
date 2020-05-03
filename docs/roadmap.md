
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
- Should we deprecate `StringTransformStep`?

**Documentation Steps**

- `DescribeStep`

**Validation Steps**

- `CheckColumnsStep`
- `CheckSameLength` for Merge Operations

**Transformers**

- Cover all the current transformers with tests
- Enhance the documentation, same structure than selectors
- `NumericRound(x, digits=1)`
- `RowNumber()`

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
