from pandas import NamedAgg
from pandas import Series

class Aggregation():
    """
    Base abstract interface to define group aggregations
    """
    def resolve(self, gdf):
        pass


class AggNumeric(Aggregation):
    """
    Base abstract interface to define numeric group aggregations
    """
    def resolve(self, gdf):
        pass


class AggMean(AggNumeric):
    """
    Calculate the mean of the grouped numeric column
    """
    def __init__(self, column):
        self.column = column

    def resolve(self, gdf):
        return NamedAgg(column=self.column, aggfunc='mean')


class AggMedian(AggNumeric):
    """
    Calculate the median of the grouped numeric column
    """
    def __init__(self, column):
        self.column = column

    def resolve(self, gdf):
        return NamedAgg(column=self.column, aggfunc='median')


class AggSum(AggNumeric):
    """
    Calculate the sum of the grouped numeric column
    """
    def __init__(self, column):
        self.column = column

    def resolve(self, gdf):
        return NamedAgg(column=self.column, aggfunc='sum')


class AggCount(AggNumeric):
    """
    Calculate the count/size of the grouped numeric column
    """
    def __init__(self, column):
        self.column = column

    def resolve(self, gdf):
        return NamedAgg(column=self.column, aggfunc='size')


class AggCountDistinct(AggNumeric):
    """
    Calculate the unique count of the grouped numeric column
    """
    def __init__(self, column):
        self.column = column

    def resolve(self, gdf):
        return NamedAgg(column=self.column, aggfunc=Series.nunique)



class AggMax(AggNumeric):
    """
    Calculate the max of the grouped numeric column
    """
    def __init__(self, column):
        self.column = column

    def resolve(self, gdf):
        return NamedAgg(column=self.column, aggfunc='max')


class AggMin(AggNumeric):
    """
    Calculate the min of the grouped numeric column
    """
    def __init__(self, column):
        self.column = column

    def resolve(self, gdf):
        return NamedAgg(column=self.column, aggfunc='min')
