
## For Beta Testing:

**Features**

- `SelectStep([AllString(), 'rating', 'year'])` Composed selections
- `GroupByStep`
- `SummarizeStep`
- `CustomStep`
- `StrRemove()` and `StrRemoveAll()`: Remove matched patterns in a string
- `LeftJoinStep(df|recipe)` and `LeftJoinStep(dfs|recipes)`

**BugFixes**

- Selectors doesn't support strings as inputs `title` != `['title']`

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

- Cover all the current transformers with tests

- Enhance the documentation, same structure than selectors
- `NumericRound(x, digits=1)`

**Selectors**

- Enhance the documentation, same structure than transformers

**Workflows**

- `InnerJoinStep(df|recipe)` and `InnerJoinStep(dfs|recipes)`
- Concatenate, Merge and Join Difference Recipes

**Library**

- Define the * exports

**Documentation**

- Prepare a Python Notebook with an end to end read example
- Improve CSS on the docstrings

**Bugs**
