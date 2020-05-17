# Methods for Creating and Transforming Variables

Besides selecting sets of existing columns, it’s often useful to add new columns that are functions
of existing columns or modify values on rows. This is the job of `MutateStep()`:

This steps uses a dictionary to list columns (keys) and transformers (values) that should be applied
while you are allowed to refer to columns that you’ve just created:

The most basic signature is the following:

```python
recipe = Recipe([
    MutateStep({
        # Column "fullname" from: "JONATHAN ARCHER" to "Jonathan Archer"
        'fullname': StrToTitle()
    })
])
```

While you can also pass a column name to transform:

```python
# Column "fullname" from: "JONATHAN ARCHER" to "Jonathan Archer"
MutateStep({'fullname': StrToTitle('fullname')})
```

Moreover, you can extend to complex chains of transformations:

```python
# Let's transform/create some variables:
MutateStep({
  # Transform the "name" column
  'name': [
      # "JONATHAN ARCHER" to "Jonathan Archer"
      StrToTitle('name'),
      # " Data " to "Data"
      StrTrim('name'),
      # "Philippa  Georgiou" to "Philippa Georgiou"
      StrReplace('  ', ' ', 'name'),
      # "Jean--Luc PICARD" to "Jean-Luc Picard"
      StrReplaceAll('--', '-', 'name')
  ],
  'rank': StrToTitle('rank')
})
```

Currently the transformers are categorized as:

- String Transformers: String Transformers provide a cohesive set of transformers designed to make working with strings as easy as possible.
- Rank Transformers: Returns the sample ranks of the values in a column.

## Available Transformers

#### String Transformers

String Transformers provide a cohesive set of transformers designed to make working with strings as easy as possible:

- [StrToUpper](#strtoupper): Convert to UPPER CASE
- [StrToLower](#strtolower): Convert to lower case
- [StrToSentence](#strtosentence): Convert to Sentence case
- [StrToTitle](#strtotitle): Convert to Title Case
- [StrTrim](#strtrim): Remove whitespaces
- [StrReplace](#strreplace): Replace first occurrence of pattern
- [StrReplaceAll](#strreplaceall): Replace all occurrences of pattern
- [StrPad](#strpad): Pad a string
- [StrSlice](#strslice): Extract and replace substrings
- [StrRemove](#strremove): Remove first matched pattern
- [StrRemoveAll](#strremoveall): Remove all matched patterns
- [StrMapValues](#strmapvalues): Replace specified values with new values.

#### Rank Transformers

Returns the sample ranks of the values in a column:

- [Rank / RankTransformer](#rank-ranktransformer): Return the sample ranks of the values
- [RowNumber](#rownumber): Return the row number
- [RankFirst](#rankfirst): Increasing rank values at each index
- [RankMin](#rankmin): Return the minimum value
- [RankMax](#rankmax): Return the maximum value
- [RankDense](#rankdense): Like `RankMin` but with no gaps between ranks
- [RankMean](#rankmean): Return the mean/average value
- [RankPercent](#rankpercent): A number between 0 and 1 computed by rescaling `RankMin` to `[0, 1]`

## Transformer Documentation

### StrToUpper

::: yeast.transformers.StrToUpper
    :docstring:

### StrToLower

::: yeast.transformers.StrToLower
    :docstring:

### StrToSentence

::: yeast.transformers.StrToSentence
    :docstring:

### StrToTitle

::: yeast.transformers.StrToTitle
    :docstring:

### StrTrim

::: yeast.transformers.StrTrim
    :docstring:

### StrReplace

::: yeast.transformers.StrReplace
    :docstring:

### StrReplaceAll

::: yeast.transformers.StrReplaceAll
    :docstring:


### StrPad

::: yeast.transformers.StrPad
    :docstring:

### StrSlice

::: yeast.transformers.StrSlice
    :docstring:

### StrRemove

::: yeast.transformers.StrRemove
    :docstring:

### StrRemoveAll

::: yeast.transformers.StrRemoveAll
    :docstring:

### StrMapValues

::: yeast.transformers.StrMapValues
    :docstring:

### Rank / RankTransformer

::: yeast.transformers.RankTransformer
    :docstring:

### RowNumber

::: yeast.transformers.RowNumber
    :docstring:

### RankFirst

::: yeast.transformers.RankFirst
    :docstring:

### RankMin

::: yeast.transformers.RankMin
    :docstring:

### RankMax

::: yeast.transformers.RankMax
    :docstring:

### RankDense

::: yeast.transformers.RankDense
    :docstring:

### RankMean

::: yeast.transformers.RankMean
    :docstring:

### RankPercent

::: yeast.transformers.RankPercent
    :docstring:


## What's next?

- [Methods for Groups and Aggregations](aggregations.md)
