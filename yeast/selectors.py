class Selector():
    """
    Base abstract interface to define column selectors
    """
    def resolve(self, df):
        pass


class AllColumns(Selector):
    """
    Return all columns on the DataFrame

    ```python
    Recipe([
        # Will keep all columns
        SelectStep(AllColumns())
    ])
    ```
    """
    def resolve(self, df):
        return df.columns.tolist()


class AllMatching(Selector):
    """
    Return all columns matching the regular expression given by `pattern`

    ```python
    Recipe([
        # Will keep all the columns ending with "ed" (ed$)
        SelectStep(AllMatching('ed$'))
    ])
    ```
    """
    def __init__(self, pattern=""):
        self.pattern = pattern

    def resolve(self, df):
        return df.filter(regex=self.pattern).columns.tolist()


class AllNumeric(Selector):
    """
    Return all numerical columns

    ```python
    Recipe([
        # Will keep all numerical values like `int`, `float`, etc.
        SelectStep(AllNumeric())
    ])
    ```
    """
    def resolve(self, df):
        return df.select_dtypes(include=['number']).columns.tolist()


class AllString(Selector):
    """
    Return all string columns

    ```python
    Recipe([
        # Will keep all strings
        SelectStep(AllString())
    ])
    ```
    """
    def resolve(self, df):
        return df.select_dtypes(include=['string']).columns.tolist()


class AllBoolean(Selector):
    """
    Return all boolean columns

    ```python
    Recipe([
        # Will keep all booleans
        SelectStep(AllBoolean())
    ])
    ```
    """
    def resolve(self, df):
        return df.select_dtypes(include=['bool']).columns.tolist()


class AllDatetime(Selector):
    """
    Return all DateTime columns

    ```python
    Recipe([
        # Will keep all dates and times
        SelectStep(AllDatetime())
    ])
    ```
    """
    def resolve(self, df):
        return df.select_dtypes(include=['datetime']).columns.tolist()


class AllCategorical(Selector):
    """
    Return all Categorical columns

    ```python
    Recipe([
        # Will keep all categorical
        SelectStep(AllCategorical())
    ])
    ```
    """
    def resolve(self, df):
        return df.select_dtypes(include=['category']).columns.tolist()
