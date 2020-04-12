## 5 Minute Introduction

# Steps

```python
CleanColumnNamesStep('snake')
```

# Recipes

```python
recipe_a = Recipe([
    ...
], inputs='dfx')

recipe_b = Recipe([
    ...
], inputs='dfy')

recipe_merge = MergeRecipe('inner_join', by=['id'])
```

# Workflows / Cookbook

```
dfx -> A -> B -----|
                 Merge -> D -> df
dfy -> C ----------|
```

```python
workflow = Workflow()
workflow >> ( recipe_a >> recipe_b ) >> merge_recipe << recipe_c << workflow
merge_recipe >> recipe_c
df = workflow.prepare_bake(inputs={
  'dfx': dfx,
  'dfy': dfy
})
```

```python
pdfx = Placeholder('dfx')
pdfy = Placeholder('dfy')

x = recipe_a(pdfa)
x = recipe_b(x)

y = recipe_c(pdfb)

z = merge_recipe(x, y)
z = recipe_d(z)

Workflow(inputs={
  'dfx': dfx,
  'dfy': dfy
}, outputs=z).prepare_bake()
```
