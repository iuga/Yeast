import pandas as pd
from yeast.step import Step
from yeast.errors import YeastRecipeError


class Recipe():
    """
    Yeast Recipe Definition:
    The recipe executes a list of steps that will be used to prepare and bake/transform the data.

    Workflow:
    For each step first we prepare it to then bake it.
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
        if not isinstance(df, pd.DataFrame):
            raise YeastRecipeError('Data must be a Pandas Data Frame')

        for step in self.steps:
            step.prepare(df)
        return self

    def bake(self, df):
        """
        Bake the recipe returning the transformed data frame.
        For each step in the recipe:
            bake the step
        """
        if not isinstance(df, pd.DataFrame):
            raise YeastRecipeError('Data must be a Pandas Data Frame')

        baked_df = df.copy()
        for step in self.steps:
            baked_df = step.bake(baked_df)
        return baked_df
