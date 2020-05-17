# San Fanciscon Crime

## Motivation

From 1934 to 1963, San Francisco was infamous for housing some of the world's most notorious criminals on the inescapable island of Alcatraz. Today, the city is known more for its tech scene than its criminal past. But, with rising wealth inequality, housing shortages, and a proliferation of expensive digital toys riding BART to work, there is no scarcity of crime in the city by the bay.

### Overview

From Sunset to SOMA, and Marina to Excelsior, this dataset provides nearly 12 years of crime reports from across all of San Francisco's neighborhoods. Given time and location, you must predict the category of crime that occurred.

### Approach

We will apply a full Data Science life cycle composed of the following steps:

- Data Wrangling to perform all the necessary actions to clean the dataset.
- Data Exploration for understanding the variables and create intuition on the data.
- Feature Engineering to create additional variables from the existing.
- Data Normalization and Data Transformation for preparing the dataset for the learning algorithms.
- Training / Testing data creation to evaluate the performance of our model.


## Data Wrangling

### Loading the data


```python
# Core imports
import pandas as pd
import numpy as np

# Yeast imports
from yeast import Recipe
from yeast.steps import *
from yeast.transformers import *
```


```python
train = pd.read_csv('sf_train.csv')
test = pd.read_csv('sf_test.csv')
```


```python
train.head(n=2)
train.shape
```

### The cleaning recipe


```python
recipe = Recipe([
    # This dataset contains 2323 duplicates that we should remove
    DropDuplicateRowsStep(),
    # Some Geolocation points are missplaced
    # We will replace the outlying coordinates with the average coordinates
    MutateStep({
        'X': MapValues({-120.5: np.NaN}),
        'Y': MapValues({90: np.NaN})
    }),
    MeanImputeStep(['X', 'Y'])
]).prepare(train)
```


```python
baked_train = recipe.bake(train)
baked_test = recipe.bake(test)
baked_train.head()
```

## Links & Resources

- [SF-Crime Analysis & Prediction by @yannisp](https://www.kaggle.com/yannisp/sf-crime-analysis-prediction)
