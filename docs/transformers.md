Transformers can modify values on rows based on some conditions and are used inside transformer steps.
The usage is quite simple, you can list them on any transformer step on the Recipe:

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

**Available Transformers:**

- `StrToUpper`, `StrToLower`, `StrToSentence`
- `StrTrim`
- `StrReplace`, `StrReplaceAll`
- `StrPad`

## String Transformers

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
