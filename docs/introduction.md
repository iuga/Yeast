# 5 Minute Introduction

Eager to get started? This part of the documentation, begins with some background information about
Yeast, then focuses on step-by-step instructions for Recipe development.

## A Minimal Recipe

A minimal Yeast Recipe looks something like this:

```python
from Yeast import Recipe, steps

recipe = Recipe([
  # Convert all columns names to Snake Case:
  steps.CleanColumnNamesStep('snake')
])

baked_df = recipe.prepare(df).bake(df)
```

So what did that code do?

- First we imported the `Recipe` class and the `steps` module. An instance of a recipe will be our
  list of steps to process data while steps contains a collection of well tested methods to
  simplify the job.
- Next we created an instance of `Recipe` that will receive a list of steps that will be executed
  sequentially in order to process and clean the data. As an example `CleanColumnNamesStep` will
  rename all columns to match the snake case convention.
- Then we used `prepare(data)` to prepare the recipe before baking (processing). Some steps require
  preparation before be baked (executed). For example: calculate the mean before imputation.
- Finally, we called `bake(data)` to execute all the steps on `data` (a Pandas DataFrame).

## The Steps

Steps are a collection of well-tested instruments that you can use without too much study in your
data processing flow because they cover a wide range of use-cases. Each one has its own signature and
specifics that you can discover on the [API reference](reference.html). One example:

```python
# Convert all columns names to Snake Case:
CleanColumnNamesStep('snake')
```

## Selectors

The [selectors](selectors.html) can select columns based on their data type or name:

```python
# Shortcut to keep only the numerical columns
SelectColumnsStep(AllNumeric())
```

## Recipes

A Recipe executes an ordered list of steps that will be used to prepare and bake/transform the data.

```python
# Define a recipe of steps to process your data
recipe = Recipe([
  # Convert all columns names to Snake Case:
  CleanColumnNamesStep('snake')
])

# Prepare the recipe
recipe = recipe.prepare(raw_data)

# Execute (bake) the recipe
clean_data = recipe.bake(raw_data)
```
## What's next?

[Methods for Selecting Variables](selectors.md)
