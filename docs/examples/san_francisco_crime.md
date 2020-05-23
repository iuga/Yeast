# San Fanciscon Crime

## Motivation

From 1934 to 1963, San Francisco was infamous for housing some of the world's most notorious criminals on the inescapable island of Alcatraz. Today, the city is known more for its tech scene than its criminal past. But, with rising wealth inequality, housing shortages, and a proliferation of expensive digital toys riding BART to work, there is no scarcity of crime in the city by the bay.

### Overview

From Sunset to SOMA, and Marina to Excelsior, this dataset provides nearly 12 years of crime reports from across all of San Francisco's neighborhoods. Given time and location, you must predict the category of crime that occurred.

### Approach

We will apply a full Data Science Development life cycle composed of the following steps:

- Data Wrangling to perform all the necessary actions to clean the dataset.
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
from yeast.selectors import *
```


```python
train = pd.read_csv('../../data/sf_train.csv')
test = pd.read_csv('../../data/sf_test.csv')
```

### The cleaning recipe


```python
recipe = Recipe([
    # Normalize all column names
    CleanColumnNamesStep('snake'),
    # This dataset contains 2323 duplicates that we should remove only on training set
    DropDuplicateRowsStep(role='training'),
    # Some Geolocation points are missplaced
    # We will replace the outlying coordinates with the average coordinates
    MutateStep({
        'x': MapValues({-120.5: np.NaN}),
        'y': MapValues({90: np.NaN})
    }),
    MeanImputeStep(['x', 'y']),
    # Extract some features drom the date:
    CastStep({'dates': 'datetime'}),
    MutateStep({
        'year': DateYear('dates'),
        'quarter': DateQuarter('dates'),
        'month': DateMonth('dates'),
        'week': DateWeek('dates'),
        'day': DateDay('dates'),
        'hour': DateHour('dates'),
        'minute': DateMinute('dates'),
        'dow': DateDayOfWeek('dates'),
        'doy': DateDayOfYear('dates')
    }),
    # Calculate the tenure: days(date - min(date)):
    MutateStep({
        'tenure': lambda df: (df['dates'] - df['dates'].min()).apply(lambda x: x.days)
    }),
    # Is it on a block?
    MutateStep({
        'is_block': StrContains('block', column='address', case=False)
    }),
    # Convert the category (target) into a numerical feature:
    # OrdinalScoreStep('category'),
    # Drop irrelevant Columns
    DropColumnsStep(['dates', 'day_of_week']),
    # Cast the numerical features
    CastStep({
        'is_block': 'integer'  # True and False to 1 and 0
    }),
    # Keep only numerical features
    SelectStep(AllNumeric()),
]).prepare(train)
```


```python
baked_train = recipe.bake(train)
baked_test  = recipe.bake(test, role="testing")
```


```python
baked_train.sample(5).head().T
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>726598</th>
      <th>144656</th>
      <th>604682</th>
      <th>680623</th>
      <th>608770</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>x</th>
      <td>-122.474</td>
      <td>-122.435</td>
      <td>-122.429</td>
      <td>-122.403</td>
      <td>-122.42</td>
    </tr>
    <tr>
      <th>y</th>
      <td>37.76</td>
      <td>37.7249</td>
      <td>37.7818</td>
      <td>37.7754</td>
      <td>37.7393</td>
    </tr>
    <tr>
      <th>year</th>
      <td>2005</td>
      <td>2013</td>
      <td>2006</td>
      <td>2005</td>
      <td>2006</td>
    </tr>
    <tr>
      <th>quarter</th>
      <td>1</td>
      <td>2</td>
      <td>4</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <th>month</th>
      <td>1</td>
      <td>6</td>
      <td>10</td>
      <td>9</td>
      <td>9</td>
    </tr>
    <tr>
      <th>week</th>
      <td>4</td>
      <td>24</td>
      <td>42</td>
      <td>38</td>
      <td>38</td>
    </tr>
    <tr>
      <th>day</th>
      <td>27</td>
      <td>13</td>
      <td>17</td>
      <td>21</td>
      <td>22</td>
    </tr>
    <tr>
      <th>hour</th>
      <td>7</td>
      <td>19</td>
      <td>10</td>
      <td>17</td>
      <td>17</td>
    </tr>
    <tr>
      <th>minute</th>
      <td>0</td>
      <td>35</td>
      <td>51</td>
      <td>30</td>
      <td>35</td>
    </tr>
    <tr>
      <th>dow</th>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>2</td>
      <td>4</td>
    </tr>
    <tr>
      <th>doy</th>
      <td>27</td>
      <td>164</td>
      <td>290</td>
      <td>264</td>
      <td>265</td>
    </tr>
    <tr>
      <th>tenure</th>
      <td>752</td>
      <td>3811</td>
      <td>1380</td>
      <td>989</td>
      <td>1355</td>
    </tr>
    <tr>
      <th>is_block</th>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



## Links & Resources

- [SF-Crime Analysis & Prediction by @yannisp](https://www.kaggle.com/yannisp/sf-crime-analysis-prediction)
