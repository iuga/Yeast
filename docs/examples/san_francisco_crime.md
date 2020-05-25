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

# Machine Learning imports
import xgboost as xgb
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
    # Drop irrelevant Columns
    DropColumnsStep(['dates', 'day_of_week']),
    # Cast the numerical features
    CastStep({
        'is_block': 'integer'  # True and False to 1 and 0
    }),
    # Convert the category (target) into a numerical feature:
    OrdinalEncoderStep('category', role='training'),
    # Keep only numerical features
    SelectStep(AllNumeric()),
]).prepare(train)
```


```python
baked_train = recipe.bake(train, role="training")
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
      <th>304544</th>
      <th>158399</th>
      <th>244432</th>
      <th>514937</th>
      <th>16967</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>category</th>
      <td>25</td>
      <td>16</td>
      <td>21</td>
      <td>16</td>
      <td>7</td>
    </tr>
    <tr>
      <th>x</th>
      <td>-122.391</td>
      <td>-122.468</td>
      <td>-122.422</td>
      <td>-122.403</td>
      <td>-122.427</td>
    </tr>
    <tr>
      <th>y</th>
      <td>37.734</td>
      <td>37.717</td>
      <td>37.7416</td>
      <td>37.7982</td>
      <td>37.7692</td>
    </tr>
    <tr>
      <th>year</th>
      <td>2011</td>
      <td>2013</td>
      <td>2012</td>
      <td>2008</td>
      <td>2015</td>
    </tr>
    <tr>
      <th>quarter</th>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>month</th>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>week</th>
      <td>10</td>
      <td>14</td>
      <td>4</td>
      <td>6</td>
      <td>8</td>
    </tr>
    <tr>
      <th>day</th>
      <td>8</td>
      <td>6</td>
      <td>28</td>
      <td>9</td>
      <td>20</td>
    </tr>
    <tr>
      <th>hour</th>
      <td>18</td>
      <td>18</td>
      <td>2</td>
      <td>0</td>
      <td>10</td>
    </tr>
    <tr>
      <th>minute</th>
      <td>0</td>
      <td>30</td>
      <td>41</td>
      <td>15</td>
      <td>43</td>
    </tr>
    <tr>
      <th>dow</th>
      <td>1</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>4</td>
    </tr>
    <tr>
      <th>doy</th>
      <td>67</td>
      <td>96</td>
      <td>28</td>
      <td>40</td>
      <td>51</td>
    </tr>
    <tr>
      <th>tenure</th>
      <td>2983</td>
      <td>3743</td>
      <td>3309</td>
      <td>1860</td>
      <td>4428</td>
    </tr>
    <tr>
      <th>is_block</th>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## Training and Validation using XGBoost


```python
features = list(set(baked_train.columns)-set(['category']))
dtrain = xgb.DMatrix(
    baked_train[features].values, 
    label=baked_train['category'], 
    feature_names=baked_train[features].columns
)
```


```python
params = {
    'max_depth': 3,
    'eta': 0.3,
    'objective': 'multi:softprob',
    'num_class': 39,
    'eval_metric': 'mlogloss'
}

history = xgb.cv(
    params=params, dtrain=dtrain, nfold=5, seed=42,
    num_boost_round=15, stratified=True, verbose_eval=False
)

history.tail()
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
      <th>train-mlogloss-mean</th>
      <th>train-mlogloss-std</th>
      <th>test-mlogloss-mean</th>
      <th>test-mlogloss-std</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>10</th>
      <td>2.482818</td>
      <td>0.000661</td>
      <td>2.485002</td>
      <td>0.002041</td>
    </tr>
    <tr>
      <th>11</th>
      <td>2.467268</td>
      <td>0.000718</td>
      <td>2.469610</td>
      <td>0.002145</td>
    </tr>
    <tr>
      <th>12</th>
      <td>2.454027</td>
      <td>0.000752</td>
      <td>2.456544</td>
      <td>0.002004</td>
    </tr>
    <tr>
      <th>13</th>
      <td>2.442648</td>
      <td>0.001062</td>
      <td>2.445381</td>
      <td>0.001881</td>
    </tr>
    <tr>
      <th>14</th>
      <td>2.433441</td>
      <td>0.001282</td>
      <td>2.436348</td>
      <td>0.001993</td>
    </tr>
  </tbody>
</table>
</div>



The above model achieved **2.433441** 5-fold cross-validation score after 10 epochs and **2.436348** on the testing set while 2.49136 was the benchmark.

### XGBoost: Feature Importance
A benefit of using gradient boosting is that after the boosted trees are constructed, it is relatively straightforward to retrieve importance scores for each attribute. Generally, importance provides a score that indicates how useful or valuable each feature was in the construction of the boosted decision trees within the model


```python
model = xgb.train(
    params=params, dtrain=dtrain, num_boost_round=15
)
```


```python
for feature, importance in model.get_score().items():
    print(f'{feature}       \t {importance}')
```

    hour       	 598
    x       	 649
    y       	 836
    is_block       	 383
    dow       	 35
    minute       	 626
    tenure       	 393
    day       	 51
    doy       	 61
    year       	 32


## Links & Resources

- [SF-Crime Analysis & Prediction by @yannisp](https://www.kaggle.com/yannisp/sf-crime-analysis-prediction)
- [Feature Importance and Feature Selection With XGBoost in Python](https://machinelearningmastery.com/feature-importance-and-feature-selection-with-xgboost-in-python/)
