# Methods for Transforming Variables

Transformers can modify values on rows based on some conditions and are used inside transformer steps.
The usage is quite simple, you can list them on any transformer step on the Recipe:

```python
# Will keep all the numeric variables
recipe = Recipe([
    StringTransformStep(columns=['name'], transformers=[
        # "JONATHAN ARCHER" to "Jonathan Archer"
        StrToTitle(),
        # " Data " to "Data"
        StrTrim(),
        # "Philippa  Georgiou" to "Philippa Georgiou"
        StrReplace('  ', ' '),
        # "Jean--Luc PICARD" to "Jean-Luc Picard"
        StrReplaceAll('--', '-')
    ])
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
