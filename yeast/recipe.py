from pandas.core.frame import DataFrame
from yeast.step import Step
from yeast.errors import YeastRecipeError, YeastBakeError, YeastValidationError
from yeast.errors import YeastTransformerError


class Recipe():
    """
    Yeast Recipe Definition:
    The recipe executes a list of steps that will be used to prepare and bake/transform the data.

    Workflow:
    For each step first we prepare it to then bake it.

    Raises:

    - `YeastRecipeError`: if there was an error with the recipe
    - `YeastBakeError`: if there was an error while baking
    - `YeastTransformerError`: if there was an error while transforming
    - `YeastValidationError`: if there was an error during step validation
    """
    def __init__(self, steps):
        steps = steps if isinstance(steps, list) else [steps]
        if not all([isinstance(step, Step) for step in steps]):
            raise YeastRecipeError("All steps must inherit from the class yeast.Step")
        self.steps = steps

    def prepare(self, df):
        """
        Prepare all the steps including validations.
        For each step in the recipe:
            prepare and validate the step
        """
        if type(df) not in [DataFrame, Recipe]:
            raise YeastRecipeError('Data must be a Pandas DataFrame or a Recipe')

        for step in self.steps:
            step.prepare(df)
        return self

    def bake(self, df):
        """
        Bake the recipe returning the transformed data frame.
        For each step in the recipe:
            bake the step
        """
        if type(df) not in [DataFrame, Recipe]:
            raise YeastRecipeError('Data must be a Pandas DataFrame or a Recipe')

        baked_df = df.copy()
        for step in self.steps:
            try:
                baked_df = step.bake(baked_df)
            except YeastRecipeError as ex:
                raise ex
            except YeastValidationError as ex:
                raise ex
            except YeastBakeError as ex:
                raise ex
            except YeastTransformerError as ex:
                raise ex
            except Exception as ex:
                raise YeastBakeError(f'There was an error while baking: {ex}') from ex
        return baked_df
