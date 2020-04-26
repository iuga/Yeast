<p align="center">
  <img src="./docs/logo.png" alt="Yeast logo">
</p>

Yeast is a Python data processing engine for modeling or visualization based on Pandas designed for reliable production data pipelines and inspired on [R Recipes](https://tidymodels.github.io/recipes/).

<p align="right">
  <img src="https://github.com/iuga/Yeast/workflows/Build/badge.svg" alt="Yeast build">
</p>

```python
from yeast import Recipe
from yeast.steps import *
from yeast.selectors import *
from yeast.transformers import *
from yeast.aggregations import *

# Define a recipe of steps to process your data
recipe = Recipe([
  # Convert all columns names to Snake Case:
  CleanColumnNamesStep('snake'),
  # More descriptive names for some columns:
  RenameColumnsStep({'uid', 'user_id'}),
  # Keep only ratings equal or bigger than 9:
  FilterStep("rating >= 9"),
  # Keep only string/text variables:
  SelectStep(AllString()),
  # The user_id column (string) need some processing
  # Example "   3a2-A" to "0003A2"
  StringTransformStep('user_id', transformers=[
    # Remove whitespaces from start and end of string
    StrTrim(),
    # The suffix "-A" should be removed
    StrReplace('-A', ''),
    # Transform to uppercase
    StrToUpper(),
    # Pad to match length
    StrPad(width=6, side='left', pad='0')
  ]),
  # Group the data by user_id
  GroupByStep(['user_id']),
  # Let's summarize the data:
  SummarizeStep({
    # Calculate the mean rating by user
    'average_rating': AggMean('rating'),
  }),
  # Sort / Arrange the results,
  SortStep(['user_id'])
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
