from yeast.errors import YeastTransformerError


class Transformer():
    """
    Base abstract interface to define column transformers.
    The column name to transform can be assigned during two phases:
    - During object definition (constructor) with presedence.
    - During resolving (resolve)

    Workflow:
    __init__ >> resolve >> do_resolve
    """
    def __init__(self, column=None):
        self.column = column

    def resolve(self, df, column=None):
        self.column = self.column if self.column else column
        if not self.column:
            raise YeastTransformerError('The selected column name to transform is empty')
        return self.do_resolve(df, self.column)

    def do_resolve(self, df, column):
        """
        Let subclasses override this operation
        """
        pass

    def set_column_if_required(self, column):
        """
        Set the column if it does not have a value.
        This should be use to double check that the destination column has a value
        """
        self.column = self.column if self.column else column

    def __call__(self, df, column=None):
        """
        Make transformers callable
        """
        return self.resolve(df, column=column)


class StrTransformer(Transformer):
    """
    Base abstract interface to define string column transformers
    """
    pass


class StrToUpper(StrTransformer):
    """
    Convert case of a string to Upper case:
    ("Yeast" to "YEAST")
    """
    def do_resolve(self, df, column):
        return df[column].str.upper()


class StrToLower(StrTransformer):
    """
    Convert case of a string to Lower case:
    ("Yeast" to "yeast")
    """
    def do_resolve(self, df, column):
        return df[column].str.lower()


class StrToSentence(StrTransformer):
    """
    Converts first character to uppercase and remaining to lowercase:
    ("yeast help" to "Yeast help")
    """
    def do_resolve(self, df, column):
        return df[column].str.capitalize()


class StrToTitle(StrTransformer):
    """
    Converts first character of each word to uppercase and remaining to lowercase:
    ("yeast help" to "Yeast Help")
    """
    def do_resolve(self, df, column):
        return df[column].str.title()


class StrTrim(StrTransformer):
    """
    Convert removing whitespaces from start and end of string:
    (" Yeast " to "Yeast")
    """
    def do_resolve(self, df, column):
        return df[column].str.strip()


class StrReplace(StrTransformer):
    """
    Replace first ocurrence of matched patterns in a string: 'Y' to 'X' ("YYY" to "XYY")

    Parameters:

    - `pattern`: Pattern or string to look for.
    - `replacement`: A string of replacements.
    """
    def __init__(self, pattern, replacement, column=None):
        super().__init__(column=column)
        self.pattern = pattern
        self.replacement = replacement

    def do_resolve(self, df, column):
        return df[column].str.replace(self.pattern, self.replacement, n=1)


class StrReplaceAll(StrTransformer):
    """
    Replace all ocurrences of matched patterns in a string: 'Y' to 'X' ("YYY" to "XXX")

    Parameters:

    - `pattern`: Pattern or string to look for.
    - `replacement`: A string of replacements.
    """
    def __init__(self, pattern, replacement, column=None):
        super().__init__(column=column)
        self.pattern = pattern
        self.replacement = replacement

    def do_resolve(self, df, column):
        return df[column].str.replace(self.pattern, self.replacement, n=-1)


class StrPad(StrTransformer):
    """
    Pad a string: 'Y' to 4 chars, left and '0' ("Y" to "000Y")

    Parameters:

    - `width`: Minimum width of padded strings.
    - `side`: Side on which padding character is added (left, right or both).
    - `pad`: Single padding character (default is a space).
    """
    def __init__(self, width, side="left", pad=" ", column=None):
        super().__init__(column=column)
        self.width = width
        self.side = side
        self.pad = pad

    def do_resolve(self, df, column):
        return df[column].str.pad(self.width, side=self.side, fillchar=self.pad)


class StrSlice(StrTransformer):
    """
    Extract and replace substrings from a string:

    ```python
    StrSlice("Yeast Help", start=6, end=10) # "Help"
    ```

    Parameters:

    - `start`: integer position of the first character
    - `stop`: integer position of the last character
    """
    def __init__(self, start, stop, column=None):
        super().__init__(column=column)
        self.start = start
        self.stop = stop

    def do_resolve(self, df, column):
        return df[column].str.slice(start=self.start, stop=self.stop)


class StrRemove(StrTransformer):
    """
    Remove first matched pattern in a string

    ```python
    StrRemove("_temp") # "Yeast_temp" to "Yeast"
    ```

    Parameters:

    - `pattern`: Pattern or string to look for.
    """
    def __init__(self, pattern, column=None):
        super().__init__(column=column)
        self.pattern = pattern

    def do_resolve(self, df, column):
        return df[column].str.replace(self.pattern, "", n=1)


class StrRemoveAll(StrTransformer):
    """
    Remove all matched patterns in a string

    ```python
    StrRemoveAll("_temp") # "Yeast_temp_temp" to "Yeast"
    ```

    Parameters:

    - `pattern`: Pattern or string to look for.
    """
    def __init__(self, pattern, column=None):
        super().__init__(column=column)
        self.pattern = pattern

    def do_resolve(self, df, column):
        return df[column].str.replace(self.pattern, "", n=-1)


class StrMapValues(StrTransformer):
    """
    Replace specified values with new values.

    ```python
    StrMapValues({'old_value': 'new_value', ...})
    ```

    Parameters:

    - `mapping`: Specify different replacement values for different existing values.
               For example: `{'old': 'new'}` replace the value `old` with `new`.
    """
    def __init__(self, mapping, column=None):
        super().__init__(column=column)
        self.mapping = mapping

    def do_resolve(self, df, column):
        return df[column].replace(self.mapping)


class RankTransformer(Transformer):
    """
    Returns the sample ranks of the values in the column.
    Ties (i.e., equal values) and missing values can be handled in several ways.

    Ties Methods:

    The `first` method results in a permutation with increasing values at each index set of ties.
    `average`, replaces them by their mean, and `max` and `min` replaces them by their maximum and
    minimum respectively. `dense` is like `min`, but with no gaps between ranks.

    Parameters:

    - `column`: name used to rank values
    - `ties_method`: string specifying how ties are treated:
                     {'average', 'min', 'max', 'first', 'dense'}
    - `ascending`: boolean with the order of the row numbers
    """
    def __init__(self, column=None, ties_method="first", ascending=True, percentage=False):
        super().__init__(column=column)
        self.ascending = ascending
        self.method = ties_method
        self.percentage = percentage
        if self.method not in ['average', 'min', 'max', 'first', 'dense']:
            raise YeastTransformerError(f'Method {ties_method} not recognized')

    def do_resolve(self, df, column):
        return df[column].rank(method=self.method, ascending=self.ascending, pct=self.percentage)


class Rank(RankTransformer):
    """
    Convenience alias for RankTransformer()
    """
    pass


class RankFirst(RankTransformer):
    """
    Increasing rank values at each index set of ties

    Parameters:

    - `ascending`: boolean with the order of the row numbers
    - `column`: used to sort/arrange and rank values
    """
    def __init__(self, column=None, ascending=True):
        super().__init__(column=column)
        self.ascending = ascending
        self.method = 'first'


class RowNumber(RankFirst):
    """
    Creates/transforms a variable containg the row number.

    Parameters:

    - `ascending`: boolean with the order of the row numbers
    - `column`: used to sort/arrange and rank values
    """
    pass


class RankMin(RankTransformer):
    """
    Replace by the minimum value

    Parameters:

    - `ascending`: boolean with the order of the row numbers
    - `column`: used to sort/arrange and rank values
    """
    def __init__(self, column=None, ascending=True):
        super().__init__(column=column)
        self.ascending = ascending
        self.method = 'min'


class RankMax(RankTransformer):
    """
    Replace by the maximum value

    Parameters:

    - `ascending`: boolean with the order of the row numbers
    - `column`: used to sort/arrange and rank values
    """
    def __init__(self, column=None, ascending=True):
        super().__init__(column=column)
        self.ascending = ascending
        self.method = 'max'


class RankDense(RankTransformer):
    """
    Replace by the minimum value like `RankMin`, but with no gaps between ranks.

    Parameters:

    - `ascending`: boolean with the order of the row numbers
    - `column`: used to sort/arrange and rank values
    """
    def __init__(self, column=None, ascending=True):
        super().__init__(column=column)
        self.ascending = ascending
        self.method = 'dense'


class RankMean(RankTransformer):
    """
    Replace by the mean/average value

    Parameters:

    - `ascending`: boolean with the order of the row numbers
    - `column`: used to sort/arrange and rank values
    """
    def __init__(self, column=None, ascending=True):
        super().__init__(column=column)
        self.ascending = ascending
        self.method = 'average'


class RankPercent(RankTransformer):
    """
    A number between 0 and 1 computed by rescaling `RankMin` to [0, 1]

    Parameters:

    - `ascending`: boolean with the order of the row numbers
    - `column`: used to sort/arrange and rank values
    """
    def __init__(self, column=None, ascending=True):
        super().__init__(column=column)
        self.ascending = ascending
        self.method = 'min'
        self.percentage = True
