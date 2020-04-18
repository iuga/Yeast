Transformers can modify values on rows based on some conditions.
The usage is quite simple, you can use them on any transformer step according to the type.

One usage example could be:
```python
# Will keep all the numeric variables
recipe = Recipe([
    StringTransformStep(columns=['name'], transformers=[
        # "JONATHAN ARCHER" to "Jonathan Archer"
        StrToSentence(),
        # " Data " to "Data"
        StrTrim(),
        # "Philippa  Georgiou" to "Philippa Georgiou"
        StrReplace('  ', ' '),
        # "Jean--Luc PICARD" to "Jean-Luc Picard"
        StrReplaceAll('--', '-')
    ])
])
```

## String Transformers

### StrToUpper()

::: yeast.transformers.StrToUpper
    :docstring:

### StrToLower()

::: yeast.transformers.StrToLower
    :docstring:

### StrToSentence()

::: yeast.transformers.StrToSentence
    :docstring:

### StrTrim()

::: yeast.transformers.StrTrim
    :docstring:

### StrReplace()

::: yeast.transformers.StrReplace
    :docstring:

### StrReplaceAll()

::: yeast.transformers.StrReplaceAll
    :docstring:
