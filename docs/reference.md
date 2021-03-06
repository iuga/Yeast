# Steps Reference

This module exposes a collection of well-tested steps that you can directly use them on your data processing pipelines.

**Columns Operations**

Execute operations over columns or predictors:

- [SelectColumnsStep](#selectcolumnsstep) / [SelectStep](#selectcolumnsstep): Select a group of columns
- [MutateStep](#mutatestep): Create or transform column values
- [RenameColumnsStep](#renamecolumnsstep): Rename column names
- [CastColumnsStep](#castcolumnsstep) / [CastStep](#castcolumnsstep): Cast the columns data types
- [DropColumnsStep](#dropcolumnsstep): Drop/Remove columns
- [DropZVColumnsStep](#dropzvcolumnsstep): Drop all columns that contain only a single value
- [CleanColumnNamesStep](#cleancolumnnamesstep): Clean all column names
- [ReplaceNAStep](#replacenastep): Replace missing values
- [OrdinalEncoderStep](#ordinalencoderstep): Encode discrete features as integer numbers

**Row Operations**

Execute operations over rows or values:

- [FilterRowsStep](#filterrowsstep) / [FilterStep](#filterrowsstep): Filter values based on a expression
- [SortRowsStep](#sortrowsstep) / [SortStep](#sortrowsstep): Sort values based on columns

**Aggregations**

Aggregate or Summarize data:

- [GroupByStep](#groupbystep): Group by rows based on columns
- [SummarizeStep](#summarizestep): Summarize the group by data
- [DropDuplicateRowsStep](#dropduplicaterowsstep) / [DropDuplicatesStep](#dropduplicaterowsstep): Drop duplicate rows

**Imputation**

Impute missing data:

- [MeanImputeStep](#meanimputestep): Impute numeric data using the mean value
- [MedianImputeStep](#medianimputestep): Impute numeric data using the median value
- [ConstantImputeStep](#constantimputestep): Impute data using a constant value

**WorkFlows**

Arrange and merge workflows and recipes

- [LeftJoinStep](#leftjoinstep): Left Join with a DataFrame or Recipe
- [RightJoinStep](#rightjoinstep): Right Join with a DataFrame or Recipe
- [InnerJoinStep](#innerjoinstep): Inner Join with a DataFrame or Recipe
- [FullJoinStep](#fulljoinstep): Full Outer Join with a DataFrame or Recipe

**Extensions**

Customize Yeast behavior for our project:

- [CustomStep](#customstep): Step to add your own functionality

# Columns Operations

## SelectColumnsStep

::: yeast.steps.SelectColumnsStep
    :docstring:

## MutateStep

::: yeast.steps.MutateStep
    :docstring:

## RenameColumnsStep

::: yeast.steps.RenameColumnsStep
    :docstring:

## CastColumnsStep

::: yeast.steps.CastColumnsStep
    :docstring:

## DropColumnsStep

::: yeast.steps.DropColumnsStep
    :docstring:

## DropZVColumnsStep

::: yeast.steps.DropZVColumnsStep
    :docstring:

## CleanColumnNamesStep

::: yeast.steps.CleanColumnNamesStep
    :docstring:

## ReplaceNAStep

::: yeast.steps.ReplaceNAStep
    :docstring:

## OrdinalEncoderStep

::: yeast.steps.OrdinalEncoderStep
    :docstring:

# Row Operations

## FilterRowsStep

::: yeast.steps.FilterRowsStep
    :docstring:

## SortRowsStep

::: yeast.steps.SortRowsStep
    :docstring:


## DropDuplicateRowsStep

::: yeast.steps.DropDuplicateRowsStep
    :docstring:

# Aggregations

## GroupByStep

::: yeast.steps.GroupByStep
    :docstring:

## SummarizeStep

::: yeast.steps.SummarizeStep
    :docstring:

# Imputation

## MeanImputeStep

::: yeast.steps.MeanImputeStep
    :docstring:

## MedianImputeStep

::: yeast.steps.MedianImputeStep
    :docstring:

## ConstantImputeStep

::: yeast.steps.ConstantImputeStep
    :docstring:

# Workflows

## LeftJoinStep

::: yeast.steps.LeftJoinStep
    :docstring:

## RightJoinStep

::: yeast.steps.RightJoinStep
    :docstring:

## InnerJoinStep

::: yeast.steps.InnerJoinStep
    :docstring:

## FullJoinStep

::: yeast.steps.FullJoinStep
    :docstring:

# Extensions

## CustomStep

::: yeast.steps.CustomStep
    :docstring:
