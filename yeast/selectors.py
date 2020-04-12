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
        return df.columns


class AllMatching(Selector):
    """
    Return all columns matching the regular expression
    """
    def __init__(self, pattern=""):
        self.pattern = pattern

    def resolve(self, df):
        return df.filter(regex=self.pattern).columns


class AllNumeric(Selector):
    """
    Return all numerical columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['number']).columns


class AllString(Selector):
    """
    Return all string columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['string']).columns


class AllBoolean(Selector):
    """
    Return all boolean columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['bool']).columns


class AllDatetime(Selector):
    """
    Return all DateTime columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['datetime']).columns


class AllCategorical(Selector):
    """
    Return all Categorical columns
    """
    def resolve(self, df):
        return df.select_dtypes(include=['category']).columns
