# Methods for Creating and Transforming Variables

Transformers can modify values on rows or create new variables based on some conditions and are
used inside transformer steps. The usage is quite simple, you can list them on any transformer step on the Recipe:

```python
recipe = Recipe([
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
])
```

**Available Transformers:**

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
