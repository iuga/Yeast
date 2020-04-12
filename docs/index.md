# Yeast

Yeast is a Python data processing engine for modeling or visualization based on Pandas designed for
reliable production data pipelines and inspired on [R Recipes](https://tidymodels.github.io/recipes/).

```python
from yeast import Recipe
from yeast.steps import CleanColumnNamesStep, SelectColumnStep
from yeast.selectors import AllNumeric

# Define a recipe of steps to process your data
recipe = Recipe([
  # Convert all columns names to Snake Case:
  CleanColumnNamesStep('snake'),
  # Keep only numerical variables:
  SelectColumnStep(AllNumeric())
])

# Prepare the recipe
recipe = recipe.prepare(raw_data)

# Execute the recipe
your_clean_data = recipe.bake(your_raw_data)
```

## What's next?

- [5 Minute Introduction](introduction.md)
- [Available Steps](steps.md)
- [Installation](install.md)

## Developers Guide

- [Steps Reference](reference.md)
- [Column Selectors](selectors.md)
