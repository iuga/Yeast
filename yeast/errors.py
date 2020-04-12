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
