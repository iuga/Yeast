# 5 Minute Introduction

Eager to get started? This part of the documentation, begins with some background information about
Yeast, then focuses on step-by-step instructions for Recipe development.

## A Minimal Recipe

The idea of a `Recipe` is to define a blueprint of data transformations that are executed
sequentially to process your data. A Recipe executes an ordered list of `Steps` that are used to
`bake`/transform your data. A minimal Yeast Recipe looks something like this:

```python
from Yeast import Recipe, steps

recipe = Recipe([
  # Convert all columns names to Snake Case:
  steps.CleanColumnNamesStep('snake'),
  # Drop duplicated rows
  steps.DropDuplicatesStep(role="training")  
])

# Prepare the recipe:
recipe = recipe.prepare(train)

# Process the training and testing set
baked_train = recipe.bake(train, role="training")
baked_test = recipe.bake(test, role="testing")
```

So what did that code do?

- First we imported the `Recipe` class and the `steps` module. An instance of a recipe will be our
  blueprint while the steps module contains a collection of well tested methods to simplify the job.
- Next we created an instance of `Recipe` that will receive a list of steps that will be executed
  sequentially in order to process and clean the data. As an example `CleanColumnNamesStep` will
  rename all columns to match the snake case convention.
- Then we used `prepare(data)` to prepare the recipe before baking (processing). Some steps require
  preparation before be baked (executed). For example: calculate the mean before imputation.
- Finally, we called `bake(data)` to execute all the steps on the `data` (a Pandas DataFrame).

What about the roles?

Roles are strings that can be used to define execution flows. By default all steps and recipes contains
the role `all`, meaning that all steps are going to be executed during `bake`. However, there are times
where we would like to circumvent some steps while baking on new data, for example, when some variables
are not available on the test set. The correct approach for this is to define a role in the step, in this
example was `DropDuplicatesStep` with `role="training"` indicating that this step will be executed when bake
has the role `all` or `training`. All other roles will skip the execution of this step, for example, `testing`.

## The Steps

Steps are a collection of well-tested instruments that you can use without too much study in your
data processing flows. Each one has its own signature and specifics that you can discover on
the [API reference](reference.html). This library will be evolving to cover more use cases.
Some example:

```python
from Yeast.steps import *

recipe = Recipe([
  # Convert all columns names to Snake Case:
  CleanColumnNamesStep('snake'),
  # Create new columns/variables:
  MutateStep({"name": StrToLower('name')}),
  # Aggregate features based on groups
  GroupByStep('city'), SummarizeStep({'total_sales': AggSum('sales')})
])
```

## Selectors

[Selectors](selectors.html) are convenience classes that you can use to select columns based on
some conditions, like their data type or name:

```python
from Yeast.selectors import *

recipe = Recipe([
  # Shortcut to keep only the numerical columns
  SelectColumnsStep(AllNumeric()),
  # Shortcut to keep only the numerical columns
  SelectColumnsStep([AllString(), AllMatching('ed$')])
])
```

## Filtering Data

In almost all of your data analysis you will need a method to filter out observations based on some
conditions. `FilterStep` provides you a straightforward approach to define those rules and execute them:

```python
from Yeast.selectors import *

recipe = Recipe([
  # Filter out all ages less than 15 and where closed_account are 1
  FilterStep('age < 15 & closed_account == 1')
])
```

## Transforming Variables

[Transformers](transformers.md) are convenience classes that you can use to transform your data or
create new variables based on those transformations. Some examples:

```Python
from Yeast.transformers import *

recipe = Recipe([
  MutateStep({
    # Replace all occurrences of "--" with "-"
    'job_title': StrReplaceAll('--', '-'),
    # Convert the name into Title Case
    'fullname': StrToTitle(),
    # Remove trail/leading whitespaces from the text
    'description': StrTrim()
  })
])
```

## Aggregations

Most data operations [are done on groups](aggregations.md) defined by columns. `GroupByStep` takes an existing dataset
and converts it into a Pandas DataFrameGroupBy where aggregation/summarization/mutation operations are
performed "by group" using `SummarizeStep`:

```Python
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

## Merging Two Datasets

In practice, you’ll normally have many tables that contribute to an analysis, and you need flexible
tools to combine them. Yeast supports [four types of joins](merge.md): left, right, inner and full:

```Python
recipe = Recipe([
  # Left join with the `sales_df` dataset the current recipe
  LeftJoinStep(sales_df, by="client_id")
])
```

## What's next?

[Methods for Selecting Variables](selectors.md)
