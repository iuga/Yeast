class Selector():
    """
    Base abstract interface to define column selectors
    """
    def resolve(self, df):
        pass


class AllColumns(Selector):
    """
    Return all columns on the DataFrame
    """
    def resolve(self, df):
        return df.columns.tolist()


class AllMatching(Selector):
    """
    Return all columns matching the regular expression given by `pattern`

    ```python
    # Will keep all the columns ending with "ed" (ed$)
    Recipe([
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
    """
    def resolve(self, df):
        return df.select_dtypes(include=['number']).columns.tolist()


class AllString(Selector):
    """
    Return all string columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['string']).columns.tolist()


class AllBoolean(Selector):
    """
    Return all boolean columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['bool']).columns.tolist()


class AllDatetime(Selector):
    """
    Return all DateTime columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['datetime']).columns.tolist()


class AllCategorical(Selector):
    """
    Return all Categorical columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['category']).columns.tolist()
