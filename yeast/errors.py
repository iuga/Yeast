class YeastValidationError(Exception):
    """
    YeastValidationError is raised when a step validation was unsuccessful.
    """
    pass


class YeastRecipeError(Exception):
    """
    YeastRecipeError is raised when there is an error on the Recipe
    """
    pass


class YeastBakeError(Exception):
    """
    YeastRecipeError is raised when there is an error while baking
    """
    pass


class YeastTransformerError(Exception):
    """
    YeastRecipeError is raised when there is an error while transforming
    """
    pass
