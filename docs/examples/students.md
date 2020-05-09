# Student Performance - Cleaning Recipe

This dataset was downloaded from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Student+Performance). This data approach student achievement in secondary education of two Portuguese schools. The data attributes include student grades, demographic, social and school related features) and it was collected by using school reports and questionnaires. Two datasets are provided regarding the performance in two distinct subjects: Mathematics (mat) and Portuguese language (por). In [Cortez and Silva, 2008], the two datasets were modeled under binary/five-level classification and regression tasks. Important note: the target attribute G3 has a strong correlation with attributes G2 and G1. This occurs because G3 is the final year grade (issued at the 3rd period), while G1 and G2 correspond to the 1st and 2nd period grades. It is more difficult to predict G3 without G2 and G1, but such prediction is much more useful (see paper source for more details).

## Importing the Libraries


```python
# General Libraries
import pandas as pd
```


```python
# Yeast specifics classes
from yeast import Recipe
from yeast.steps import *
```

## Getting the Data


```python
math_df = pd.read_csv('student-mat.csv', sep=";")
port_df = pd.read_csv('student-por.csv', sep=";")
```


```python
math_df.head(1)
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
      <th>school</th>
      <th>sex</th>
      <th>age</th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>Medu</th>
      <th>Fedu</th>
      <th>Mjob</th>
      <th>Fjob</th>
      <th>...</th>
      <th>famrel</th>
      <th>freetime</th>
      <th>goout</th>
      <th>Dalc</th>
      <th>Walc</th>
      <th>health</th>
      <th>absences</th>
      <th>G1</th>
      <th>G2</th>
      <th>G3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GP</td>
      <td>F</td>
      <td>18</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>at_home</td>
      <td>teacher</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>6</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 33 columns</p>
</div>




```python
port_df.head(1)
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
      <th>school</th>
      <th>sex</th>
      <th>age</th>
      <th>address</th>
      <th>famsize</th>
      <th>Pstatus</th>
      <th>Medu</th>
      <th>Fedu</th>
      <th>Mjob</th>
      <th>Fjob</th>
      <th>...</th>
      <th>famrel</th>
      <th>freetime</th>
      <th>goout</th>
      <th>Dalc</th>
      <th>Walc</th>
      <th>health</th>
      <th>absences</th>
      <th>G1</th>
      <th>G2</th>
      <th>G3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GP</td>
      <td>F</td>
      <td>18</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>at_home</td>
      <td>teacher</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>11</td>
      <td>11</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 33 columns</p>
</div>



## Cleaning the Data

### Defining the processing Recipe


```python
recipe = Recipe([
    # All column names to snake case
    CleanColumnNamesStep('snake'),
    # Rename columns with better names
    RenameColumnsStep({
        'famsize': 'family_size',
        'pstatus': 'parent_status',
        'medu': 'mother_education',
        'fedu': 'father_education',
        'mjob': 'mother_job',
        'fjob': 'father_job',
        'traveltime': 'travel_time',
        'studytime': 'study_time',
        'schoolsup': 'school_support',
        'famsup': 'family_support',
        'famrel': 'family_relationship_quality',
        'freetime': 'free_time',
        'goout': 'go_out_friends',
        'Dalc': 'workday_alcohol_consumption',
        'Walc': 'weekend_alcohol_consumption',
    })
])
```

### Preparing the recipe


```python
recipe = recipe.prepare(math_df)
```

### Bake / Execute the recipe 


```python
baked_math_df = recipe.bake(math_df) 
baked_port_df = recipe.bake(port_df) 
```


```python
baked_math_df.head(1)
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
      <th>school</th>
      <th>sex</th>
      <th>age</th>
      <th>address</th>
      <th>family_size</th>
      <th>parent_status</th>
      <th>mother_education</th>
      <th>father_education</th>
      <th>mother_job</th>
      <th>father_job</th>
      <th>...</th>
      <th>family_relationship_quality</th>
      <th>free_time</th>
      <th>go_out_friends</th>
      <th>dalc</th>
      <th>walc</th>
      <th>health</th>
      <th>absences</th>
      <th>g1</th>
      <th>g2</th>
      <th>g3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GP</td>
      <td>F</td>
      <td>18</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>at_home</td>
      <td>teacher</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>6</td>
      <td>5</td>
      <td>6</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 33 columns</p>
</div>




```python
baked_port_df.head(1)
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
      <th>school</th>
      <th>sex</th>
      <th>age</th>
      <th>address</th>
      <th>family_size</th>
      <th>parent_status</th>
      <th>mother_education</th>
      <th>father_education</th>
      <th>mother_job</th>
      <th>father_job</th>
      <th>...</th>
      <th>family_relationship_quality</th>
      <th>free_time</th>
      <th>go_out_friends</th>
      <th>dalc</th>
      <th>walc</th>
      <th>health</th>
      <th>absences</th>
      <th>g1</th>
      <th>g2</th>
      <th>g3</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>GP</td>
      <td>F</td>
      <td>18</td>
      <td>U</td>
      <td>GT3</td>
      <td>A</td>
      <td>4</td>
      <td>4</td>
      <td>at_home</td>
      <td>teacher</td>
      <td>...</td>
      <td>4</td>
      <td>3</td>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>11</td>
      <td>11</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 33 columns</p>
</div>


