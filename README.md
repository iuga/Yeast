# Yeast

Yeast is a Python data processing engine for modeling or visualization based on Pandas designed for reliable production data pipelines and inspired on [R Recipes](https://tidymodels.github.io/recipes/).

```python
from yeast import Recipe
from yeast.steps import *
from yeast.selectors import AllNumeric

# Define a recipe of steps to process your data
recipe = Recipe([
  # Convert all columns names to Snake Case:
  CleanColumnNamesStep('snake'),
  # More descriptive names for some columns
  RenameColumnsStep({'n_tkts', 'tickets_number'}),
  # Keep only numerical variables:
  SelectStep(AllNumeric()),
  # Keep only ratings equal or bigger than 9:
  FilterStep("rating >= 9"),
  # Sort / Arrange the results,
  SortStep(['rating'])
])

# Prepare the recipe
recipe = recipe.prepare(raw_data)

# Execute the recipe
your_clean_data = recipe.bake(your_raw_data)
```

## Installation

```
pip install git+https://github.com/iuga/Yeast
```

## What Next?

Please read the [library documentation here](https://iuga.github.io/Yeast/)
