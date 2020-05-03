# Methods for Creating and Transforming Variables

Besides selecting sets of existing columns, it’s often useful to add new columns that are functions
of existing columns or modify values on rows. This is the job of `MutateStep()`:

This steps uses a dictionary to list columns (keys) and transformers (values) that should be applied
while you are allowed to refer to columns that you’ve just created:

The most basic signature is the following:

```python
recipe = Recipe([
    MutateStep({
        # "JONATHAN ARCHER" to "Jonathan Archer"
        'name': StrToTitle('name')
    })
])
```

But you can extend to complex chains of transformations:

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

## Available Transformers

### String Transformers

- ::: yeast.transformers.StrToUpper
    :docstring:
- ::: yeast.transformers.StrToLower
    :docstring:
- ::: yeast.transformers.StrToSentence
    :docstring:
- ::: yeast.transformers.StrToTitle
    :docstring:
- ::: yeast.transformers.StrTrim
    :docstring:
- ::: yeast.transformers.StrReplace
    :docstring:
- ::: yeast.transformers.StrReplaceAll
    :docstring:
- ::: yeast.transformers.StrPad
    :docstring:
- ::: yeast.transformers.StrSlice
    :docstring:
- ::: yeast.transformers.StrRemove
    :docstring:
- ::: yeast.transformers.StrRemoveAll
    :docstring:

## What's next?

- [Methods for Groups and Aggregations](aggregations.md)
