from yeast.step import Step
from yeast.errors import YeastValidationError


class FilterRowsStep(Step):
    """
    Step in charge of filtering out rows based on boolean conditions.

    Operators:

    - `&`, `|`, `and`, `or`,  `(`, `)`
    - `in`, `not in`, `==`, `!=`, `>`, `<`, `<=`, `>=`
    - `+`, `~`, `not`

    Notes:

    - You can refer to column names with spaces or operators by surrounding them in backticks.
    - You can refer to variables in the environment by prefixing them with an ‘@’ like `@a + b`.

    Parameters:

    - `expression`: The query string to evaluate.
    - `role`: String name of the role to control baking flows on new data. Default: `all`.

    Usage:

    ```python
    # Subset a DataFrame based on a numeric variable
    FilterRowsStep('age > 20')

    # Subset a DataFrame based on a categorical / string variable
    FilterRowsStep('category == "Sci-Fi"')

    # Subset a DataFrame comparing two columns
    FilterRowsStep('seasons > rating')

    # Subset based on Multiple comparisons
    FilterRowsStep('(watched == True) and seasons in [2, 7]')

    # Subset referencing local variables inside the filter
    was_watched = False
    FilterRowsStep('watched == @was_watched')

    # Subset referencing a column name that contain spaces with backtick:
    FilterRowsStep('\`episode title\\` == "Hello"')
    ```

    Raises:

    - `YeastValidationError`: if the expression is an empty string.
    """
    def __init__(self, expression, role='all', **kwargs):
        self.expression = expression
        self.kwargs = kwargs
        super().__init__(needs_preparation=False, role=role)

    def do_bake(self, df):
        return df.query(expr=self.expression, **self.kwargs)

    def do_validate(self, df):
        """
        Validations:
        - Check that expression is not empty
        """
        if not isinstance(self.expression, str) or self.expression.strip() == '':
            raise YeastValidationError('The expression must be a non empty string')


class FilterStep(FilterRowsStep):
    """
    FilterStep is an Alias for FilterRowsStep
    """
    pass
