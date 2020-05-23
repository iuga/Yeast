from pandas.core.frame import DataFrame
from yeast.step import Step
from yeast.errors import YeastRecipeError, YeastBakeError, YeastValidationError
from yeast.errors import YeastPreparationError
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
        Prepare all the steps including validations (if required).
        For each step in the recipe:
            If the recipe needs preparation:
                - prepare the step
                - bake the step
        """
        if not isinstance(df, (DataFrame, Recipe)):
            raise YeastRecipeError('Data must be a Pandas DataFrame or a Recipe')

        if self.needs_preparation():
            prep_df = df.copy()
            for step in self.steps:
                try:
                    step.prepare(prep_df)
                    prep_df = step.bake(prep_df)
                except YeastRecipeError as ex:
                    raise ex
                except YeastValidationError as ex:
                    raise ex
                except YeastBakeError as ex:
                    raise ex
                except YeastTransformerError as ex:
                    raise ex
                except Exception as ex:
                    raise YeastPreparationError(f'There was an error while preparing: {ex}') from ex
        return self

    def bake(self, df, role='all'):
        """
        Bake the recipe returning the transformed data frame.



        Parameters:

        - `df`: DataFrame to bake
        - `role`: String name of the role to control baking flows on new data. Default: `all` to
                  execute all steps in the recipe. The role support any name that you want to use.
                  For example, if `role='train'` will execute all steps with role 'all' or 'train'
                  but all other roles will be skipped.
        """
        if not isinstance(df, (DataFrame, Recipe)):
            raise YeastRecipeError('Data must be a Pandas DataFrame or a Recipe')

        baked_df = df.copy()
        for step in self.steps:
            try:
                if role == 'all' or step.role == 'all' or role == step.role:
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

    def needs_preparation(self):
        """
        Scan all steps in this recipe to detect if any of the steps require preparation
        """
        return any([s.needs_preparation for s in self.steps])
