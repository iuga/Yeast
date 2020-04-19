
## Short-term roadmap:

**Row and Column Operations**

- `GroupByStep`
- `SummarizeStep`
- `MutateStep`
- `DropZVColumnsStep`
- `SelectStep(AllString(), 'rating', 'year')` Composed selections

**Individual Transformations**

- `ColumnMapValuesStep`
- `ColumnStringReplaceStep`

**Documentation Steps**

- `DescribeStep`

**Validation Steps**

- `CheckColumnsStep`

**Transformers**

- Cover all the current transformers with tests
- `StrRemove()` and `StrRemoveAll()`: Remove matched patterns in a string
- Enhance the documentation, same structure than selectors

**Selectors**

- Enhance the documentation, same structure than transformers

**Workflows**

- `LeftJoinStep(df|recipe)`
- `InnerJoinStep(df|recipe)`
- Concatenate, Merge and Join Difference Recipes

**Documentation**

- Prepare a Python Notebook with an end to end read example
- Improve CSS on the docstrings

**BugFixes**

- Selectors doesn't support strings as inputs `title` != `['title']`
