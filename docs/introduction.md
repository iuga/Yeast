## Installation

The basic [installation](install.html) is straightforward: 

```bash
pip install git+https://github.com/iuga/Yeast
```

## Steps

Steps are a collection of well-tested instruments that you can use without too much study in your
data processing flow because they cover a wide range of use-cases. Each one has its own signature and
specifics that you can discover on the [API reference](step_reference.html). One example:

```python
# Convert all columns names to Snake Case:
CleanColumnNamesStep('snake')
```

## Selectors

The [selectors](selectors.html) can choose columns based on their data type or name:

```python
# Shortcut to keep only the numerical columns
SelectColumnStep(AllNumeric())
```

## Recipes

A Recipe executes an ordered list of steps that will be used to prepare and bake/transform the data.

```python
# Define a recipe of steps to process your data
recipe = Recipe([
  # Convert all columns names to Snake Case:
  CleanColumnNamesStep('snake')
])
# Execute the recipe
clean_data = recipe.prepare(raw_data).bake(raw_data)
```
