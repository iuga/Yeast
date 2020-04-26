# Methods for Selecting Variables

The step to select variables from a DataFrame is `SelectColumnsStep` / `SelectStep`.
It will keep columns based on their names or the results of the selectors.

```python
from yeast.selectors import AllNumeric

Recipe([
  # AllNumeric() is a selector in charge of keep all numeric variables
  # So, when executed it keeps all numeric columns and title
  SelectStep([AllNumeric(), 'title'])
])
```

The selectors can choose columns based on their data type or name.
They are shortcuts to select a subset of columns/predictors based on a common attribute:

- `AllColumns`
- `AllString`
- `AllBoolean`
- `AllNumeric`
- `AllDatetime`
- `AllCategorical`
- `AllMatching`

The usage is quite simple, you can pass them on any parameter that indicates column names and
basically they are used to select columns based on the attributes.

```python
Recipe([
  # Will keep all numeric and 2 more columns:
  SelectStep([AllNumeric(), 'title', 'aired']),
  # Will keep all the numeric variables:
  SelectStep(AllNumeric()),
  # Will only one columns:
  SelectStep('seasons')
])
```


**Available Selectors:**

- ::: yeast.selectors.AllColumns
    :docstring:
- ::: yeast.selectors.AllString
    :docstring:
- ::: yeast.selectors.AllBoolean
    :docstring:
- ::: yeast.selectors.AllNumeric
    :docstring:
- ::: yeast.selectors.AllDatetime
    :docstring:
- ::: yeast.selectors.AllCategorical
    :docstring:
- ::: yeast.selectors.AllMatching
    :docstring:

## What's next?

[Methods for Transforming Variables](transformers.md)
