from yeast.step import Step
from yeast.errors import YeastValidationError


class CustomStep(Step):
    """
    Custom Step was designed to extend all the power of Yeast Pipelines and cover all scenarios
    where the Yeast steps are not adequate. You might need to define your own operations.
    You could define your custom transformations, business rules or extend to third-party libraries.
    The usage is quite straightforward and designed to avoid spending too much time on the
    implementation. It expects between 1 and 3 arguments, all functions and optional:

    - `to_validate(step, df)`
    - `to_prepare(step, df)`: returns `df`
    - `to_bake(step, df)`: returns `df`

    Please notice that `to_prepare` and `to_bake` must return a `DataFrame` to continue the pipeline
    execution in further steps. `CustomStep` enables you to structure and document your code and
    business rules in Steps that could be shared across Recipes.

    Parameters:

    - `to_validate`: perform validations on the data. Raise YeastValidationError on a problem.
    - `to_prepare`: prepare the step before bake, like train or calculate aggregations.
    - `to_bake`: execute the bake (processing). This is the core method.

    Inline Usage:

    ```python
    recipe = Recipe([
        # Custom Business Rules:
        CustomStep(to_bake=lambda step, df: df['sales'].fillna(0))
    ])
    ```

    Custom rules:

    ```python
    def my_bake(step, df):
        # Calculate total sales or anything you need:
        df['total_sales'] = df['sales'] + df['fees']
        return df

    recipe = Recipe([
        # Custom Business Rules:
        CustomStep(to_bake=my_bake)
    ])
    ```

    Custom Checks and Validations:

    ```python
    def my_validate(step, df):
        if 'sales' not in df.columns:
            raise YeastValidationError('sales column not found')
        if 'fees' not in df.columns:
            raise YeastValidationError('fees colum not found')

    recipe = Recipe([
        CustomStep(to_validate=my_validate, to_bake=my_bake)
    ])
    ```

    Define the Estimation/Preparation procedure:

    ```python
    def my_preparation(step, df):
        step.mean_sales = df['sales'].mean()

    def my_bake(step, df):
        df['sales_deviation'] = df['sales'] - step.mean_sales
        return df

    recipe = Recipe([
        CustomStep(to_prepare=my_preparation, to_bake=my_bake)
    ])
    ```

    Creating a custom step inheriting from CustomStep:

    ```python
    class MyCustomStep(CustomStep):

        def do_validate(self, df):
            # Some validations that could raise YeastValidationError
            pass

        def do_prepare(self, df):
            # Prepare the step if needed
            return df

        def do_bake(self, df):
            # Logic to process the df
            return df
    ```
    ```python
    recipe = Recipe([
        MyCustomStep()
    ])
    ```

    Raises:

    - `YeastValidationError`: if any of the parameters is defined but not callable.
    """
    def __init__(self, to_prepare=None, to_bake=None, to_validate=None):
        self.to_prepare = to_prepare
        self.to_bake = to_bake
        self.to_validate = to_validate

    def do_prepare(self, df):
        """
        Perform custom prepare. Expected signature (step/self, dataframe)
        """
        if self.to_prepare:
            return self.to_prepare(self, df)
        return df

    def do_bake(self, df):
        """
        Perform custom bake. Expected signature (step/self, dataframe)
        """
        if self.to_bake:
            return self.to_bake(self, df)
        return df

    def do_validate(self, df):
        """
        Perform custom validations. Expected signature (step/self, dataframe)
        - Validate that all parameters are callables or none
        - Call to perform all custom validations
        """
        if self.to_prepare is not None and not callable(self.to_prepare):
            raise YeastValidationError('to_prepare must be a function like: to_prepare(step, df)')
        if self.to_bake is not None and not callable(self.to_bake):
            raise YeastValidationError('to_bake must be a function like: to_bake(step, df)')
        if self.to_validate is not None and not callable(self.to_validate):
            raise YeastValidationError('to_validate must be a function like: to_validate(step, df)')
        if self.to_validate:
            self.to_validate(self, df)
