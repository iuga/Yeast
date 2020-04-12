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
# Will keep all the numeric variables
Recipe([
  SelectColumnStep(columns=AllNumeric())
]).prepare(data).bake(data)
```

## `AllColumns`

Returns all the current columns in the DataFrame

## `AllString`

Return all the string columns in the DataFrame. The dtype must be string, not object.

## `AllBoolean`

Returns all the boolean columns in the DataFrame.

## `AllNumeric`

Returns all the numerical columns in the DataFrame.

## `AllDatetime`

Returns all the datetime columns in the DataFrame.


## `AllCategorical`

Returns all the categorical columns in the DataFrame.

## `AllMatching`

Returns all the columns that match the regular expression passed as parameter

```python
# Will keep all the columns ending with "ed" (ed$)
Recipe([
  SelectColumnStep(columns=AllMatching('ed$'))
]).prepare(data).bake(data)
```
