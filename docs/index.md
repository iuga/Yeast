# Yeast

Yeast is a Python data processing engine for modeling or visualization based on Pandas designed for
reliable production data pipelines and inspired on [R Recipes](https://tidymodels.github.io/recipes/).

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
  # The user_id column (string) need some processing
  # Example "   3a2-A" to "0003A2"
  StringTransformStep('user_id', transformers=[
    # Remove whitespaces from start and end of string
    StrTrim(),
    # The suffix "-A" should be removed
    StrReplace('-A', ''),
    # Transform to upercase
    StrToUpper()
  ]),
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

## What's next?

- [5 Minute Introduction](introduction.md)
- [Available Steps](steps.md)
- [Installation](install.md)

## Developers Guide

- [Steps Reference](reference.md)
- [Column Selectors](selectors.md)
- [Transforming Variables](transformers.md)
