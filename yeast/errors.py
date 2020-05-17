class YeastValidationError(Exception):
    """
    YeastValidationError is raised when a step validation was unsuccessful.
    """
    pass


class YeastRecipeError(Exception):
    """
    YeastRecipeError is raised when there was an error on the Recipe
    """
    pass


class YeastPreparationError(Exception):
    """
    YeastPreparationError is raised when there was an error on the recipe preparation
    """
    pass


class YeastBakeError(Exception):
    """
    YeastRecipeError is raised when there was an error while baking
    """
    pass


class YeastTransformerError(Exception):
    """
    YeastRecipeError is raised when there was an error while transforming
    """
    pass


class YeastCookbookError(Exception):
    """
    YeastCookbookError is raised when there was an error on the cookbook
    """
    pass
