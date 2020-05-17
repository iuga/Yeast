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

- [AllColumns](#allcolumns): All variables
- [AllString](#allstring): All string variables
- [AllBoolean](#allboolean): All boolean variables
- [AllNumeric](#allnumeric): All numerical variables
- [AllDatetime](#alldatetime): All date or time variables
- [AllCategorical](#allcategorical): All categorical variables
- [AllMatching](#allmatching): All variables matching the regular expression

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


## Available Selectors

### AllColumns

::: yeast.selectors.AllColumns
    :docstring:

### AllString

::: yeast.selectors.AllString
    :docstring:

### AllBoolean

::: yeast.selectors.AllBoolean
    :docstring:

### AllNumeric

::: yeast.selectors.AllNumeric
    :docstring:

### AllDatetime

::: yeast.selectors.AllDatetime
    :docstring:

### AllCategorical

::: yeast.selectors.AllCategorical
    :docstring:

### AllMatching

::: yeast.selectors.AllMatching
    :docstring:

## What's next?

- [Methods for Transforming Variables](transformers.md)
