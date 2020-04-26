# Available Steps

## Column Operations

Execute operations over columns or predictors:

- [SelectColumnsStep](reference.html#selectcolumnsstep): Select a group of columns
- [RenameColumnsStep](reference.html#renamecolumnsstep): Rename column names
- [CleanColumnNamesStep](reference.html#cleancolumnnamesstep): Clean all column names
- [CastColumnsStep](reference.html#castcolumnsstep): Cast the columns data types
- [DropColumnsStep](reference.html#dropcolumnsstep): Drop/Remove columns

## Row Operations

Execute operations over rows or values:

- [FilterRowsStep](reference.html#filterrowsstep): Filter values based on a expression
- [SortRowsStep](reference.html#sortrowsstep): Sort values based on columns

## Aggregations

Aggregate or Summarize data:

- [GroupByStep](reference.md#groupbystep): Group by rows based on columns
- [SummarizeStep](reference.md#summarizestep): Summarize the group by data

## WorkFlows

Arrange and merge workflows and recipes

- [LeftJoinStep](reference.md#leftjoinstep): Left Join with a DataFrame or Recipe

## Extensions

Customize Yeast behavior for our project:

- [CustomStep](reference.md#customstep): Step to add your own functionality

## Step Shortcuts

Aliases for the most important Steps:

- [SelectStep](reference.html#selectcolumnsstep) alias of [SelectColumnsStep](reference.html#selectcolumnsstep)
- [FilterStep](reference.html#filterrowsstep) alias of [FilterRowsStep](reference.html#filterrowsstep)
- [SortStep](reference.html#sortrowsstep) alias of [SortRowsStep](reference.html#sortrowsstep)
- [CastStep](reference.html#castcolumnsstep) alias of [CastColumnsStep](reference.html#castcolumnsstep)

## What's next?

- [Steps API Reference](reference.md)
- [Custom Steps](extensions.md)
