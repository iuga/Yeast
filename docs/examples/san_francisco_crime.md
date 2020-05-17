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




    (878049, 9)



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
#     s.MeanInputeStep('X'),
#     s.MeanInputeStep('Y'),
])
```


```python
baked_train = recipe.prepare(train).bake(train)
baked_train.head()
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
      <th>Dates</th>
      <th>Category</th>
      <th>Descript</th>
      <th>DayOfWeek</th>
      <th>PdDistrict</th>
      <th>Resolution</th>
      <th>Address</th>
      <th>X</th>
      <th>Y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2015-05-13 23:53:00</td>
      <td>WARRANTS</td>
      <td>WARRANT ARREST</td>
      <td>Wednesday</td>
      <td>NORTHERN</td>
      <td>ARREST, BOOKED</td>
      <td>OAK ST / LAGUNA ST</td>
      <td>-122.425892</td>
      <td>37.774599</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2015-05-13 23:53:00</td>
      <td>OTHER OFFENSES</td>
      <td>TRAFFIC VIOLATION ARREST</td>
      <td>Wednesday</td>
      <td>NORTHERN</td>
      <td>ARREST, BOOKED</td>
      <td>OAK ST / LAGUNA ST</td>
      <td>-122.425892</td>
      <td>37.774599</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2015-05-13 23:33:00</td>
      <td>OTHER OFFENSES</td>
      <td>TRAFFIC VIOLATION ARREST</td>
      <td>Wednesday</td>
      <td>NORTHERN</td>
      <td>ARREST, BOOKED</td>
      <td>VANNESS AV / GREENWICH ST</td>
      <td>-122.424363</td>
      <td>37.800414</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2015-05-13 23:30:00</td>
      <td>LARCENY/THEFT</td>
      <td>GRAND THEFT FROM LOCKED AUTO</td>
      <td>Wednesday</td>
      <td>NORTHERN</td>
      <td>NONE</td>
      <td>1500 Block of LOMBARD ST</td>
      <td>-122.426995</td>
      <td>37.800873</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2015-05-13 23:30:00</td>
      <td>LARCENY/THEFT</td>
      <td>GRAND THEFT FROM LOCKED AUTO</td>
      <td>Wednesday</td>
      <td>PARK</td>
      <td>NONE</td>
      <td>100 Block of BRODERICK ST</td>
      <td>-122.438738</td>
      <td>37.771541</td>
    </tr>
  </tbody>
</table>
</div>



## Links & Resources

- [SF-Crime Analysis & Prediction by @yannisp](https://www.kaggle.com/yannisp/sf-crime-analysis-prediction)


```python
baked_train.query('Y == 90')
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
      <th>Dates</th>
      <th>Category</th>
      <th>Descript</th>
      <th>DayOfWeek</th>
      <th>PdDistrict</th>
      <th>Resolution</th>
      <th>Address</th>
      <th>X</th>
      <th>Y</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>




```python

```
