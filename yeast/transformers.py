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
