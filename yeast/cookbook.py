from yeast.recipe import Recipe
from yeast.errors import YeastCookbookError


class Cookbook():
    """
    Recipe Cookbook implements a storage for all recipes often used throughout your aaplication.

    Usage:

    ```python
    from yeast import Cookbook

    cookbook = Cookbook()
    cookbook.add('prices.cleaning.raw.v1', prices_recipe)

    cookbook.list()
    # ['prices.cleaning.raw.v1']

    prices_recipe = cookbook.get('prices.cleaning.raw.v1')
    ```
    """
    def __init__(self):
        self.book = {}

    def add(self, name, recipe):
        """
        Register any Recipe into the Cookbook.

        Parameters:

        - `name`: String name of the recipe
        - `recipe`: Recipe object you want to register

        Raises:

        - `YeastCookbookError`: if any of the parameters is incorrect
        """
        if not isinstance(name, str):
            raise YeastCookbookError('Recipe name must be a string')
        if name in self.book:
            raise YeastCookbookError(f'Recipe "{name}" already registered.')
        if not isinstance(recipe, Recipe):
            raise YeastCookbookError(f'Recipe must be a Recipe object')
        self.book[name] = recipe
        return self

    def get(self, name):
        """
        Return the recipe by name

        Parameters:

        - `name`: String with the name of the Recipe
        """
        if not isinstance(name, str):
            raise YeastCookbookError(f'Recipe name must be a string.')
        if name not in self.book:
            raise YeastCookbookError(f'Recipe "{name}" not found on this Cookbook.')
        return self.book.get(name)

    def list(self):
        """
        Get a list of all the Recipes
        """
        return self.book.keys()

        def __rshift__(self, next_stage):
        """
        Implements Self >> Next_Stage == self.set_next(next_stage)
        """
        self.set_next(next_stage)
        return next_stage

    def __rshift__(self, next_recipe):
        """
        Cookbook >> Next Recipe
        """
        self.set_next(next_stage)
        return next_stage

    def __lshift__(self, previous_recipe):
        """
        Previous Recipe << Cookbook
        """
        self.set_previous(previous_stage)
        return previous_stage
