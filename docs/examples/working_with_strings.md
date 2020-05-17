# Working With Strings

The following dataset contains users and codes. It's a real use case example of a Data Science project I worked with when having tools to work with strings is fundamental. The idea is simple, you have a list of users with a code. The code have different meanings because each letter in each position represents something different. For this example we are going to focus in one explanation, the program name. The rules:

- The code should always have 5 letters, by default `N`
- If the first letter is `A` (account) then the third letter contains the Program name.
- The Program names are: `G` Gold, `P` Platinum, and `B` Black.

Let's answer the most basic question: How many accounts per type do they have?

## Importing the Libraries


```python
# General Libraries
import pandas as pd
```


```python
# Yeast specifics classes
from yeast import Recipe
from yeast.steps import *
from yeast.transformers import *
from yeast.aggregations import *
```

## Getting the Data


```python
codes = pd.read_csv('string_codes.csv')
codes.head()
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
      <th>user</th>
      <th>code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>NNNNN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>ANPNN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>A B</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>ANPNN</td>
    </tr>
  </tbody>
</table>
</div>



## Cleaning the Data
### Defining the processing Recipe


```python
recipe = Recipe([
    # Trap: the column "code" on the csv is "  code"
    # Cleaning the column names should fix this
    CleanColumnNamesStep('snake'),
    # Replace the missing values by 'NNNNN' (no code)
    ReplaceNAStep('code', 'NNNNN'),
    # Let's clean the Code according to the business rules:
    MutateStep({
        # Transform the "name" column
        'code': [
            # No whitespace to the left or right of the string
            StrTrim(),
            # The code must have 5 characters, 'N' if no information
            StrPad(5, side='right', pad='N'),
            # Whitespaces are also coded as 'N',
            StrReplaceAll(' ', 'N')
        ],
        # Extract the first letter of the code (Account)
        'code_account': StrSlice(0, 1, column='code'),
        # Extract the third letter of the code (Account Type) if Account == 'A'
        'code_type': StrSlice(2, 3, column='code'),
        # Map the codes to the correct promotion name
        'program_name': MapValues({
            'G': 'Gold',
            'P': 'Platinum',
            'B': 'Black'
        }, column='code_type')
    })
])
```


```python
recipe = recipe.prepare(codes)
```


```python
clean_codes = recipe.bake(codes)
clean_codes.head()
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
      <th>user</th>
      <th>code</th>
      <th>code_account</th>
      <th>code_type</th>
      <th>program_name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>NNNNN</td>
      <td>N</td>
      <td>N</td>
      <td>N</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>NNNNN</td>
      <td>N</td>
      <td>N</td>
      <td>N</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>ANPNN</td>
      <td>A</td>
      <td>P</td>
      <td>Platinum</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>ANBNN</td>
      <td>A</td>
      <td>B</td>
      <td>Black</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>ANPNN</td>
      <td>A</td>
      <td>P</td>
      <td>Platinum</td>
    </tr>
  </tbody>
</table>
</div>



### How many types of accounts do they have?


```python
group_recipe = Recipe([
    # Keep Only Accounts with Type
    FilterStep('code_account == "A"'),
    # Group by Type
    GroupByStep('program_name'),
    # Count the types
    SummarizeStep({
        'program_name_count': AggCount('code_type')
    }),
    # Sort by count
    SortStep('program_name_count', ascending=False)
])
```


```python
group_codes = group_recipe.bake(clean_codes)
group_codes.head(n=15)
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
      <th>program_name</th>
      <th>program_name_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Gold</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Platinum</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Black</td>
      <td>3</td>
    </tr>
  </tbody>
</table>
</div>


