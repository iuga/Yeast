class Transformer():
    """
    Base abstract interface to define column transformers
    """
    def resolve(self, column):
        pass


class StrTransformer(Transformer):
    """
    Base abstract interface to define string column transformers
    """
    def resolve(self, column):
        pass


class StrToUpper(StrTransformer):
    """
    Convert case of a string to Upper case:
    ("Yeast" to "YEAST")
    """
    def resolve(self, column):
        return column.str.upper()


class StrToLower(StrTransformer):
    """
    Convert case of a string to Lower case:
    ("Yeast" to "yeast")
    """
    def resolve(self, column):
        return column.str.lower()


class StrToSentence(StrTransformer):
    """
    Converts first character to uppercase and remaining to lowercase:
    ("yeast help" to "Yeast help")
    """
    def resolve(self, column):
        return column.str.capitalize()


class StrToTitle(StrTransformer):
    """
    Converts first character of each word to uppercase and remaining to lowercase:
    ("yeast help" to "Yeast Help")
    """
    def resolve(self, column):
        return column.str.title()


class StrTrim(StrTransformer):
    """
    Convert removing whitespaces from start and end of string:
    (" Yeast " to "Yeast")
    """
    def resolve(self, column):
        return column.str.strip()


class StrReplace(StrTransformer):
    """
    Replace first ocurrence of matched patterns in a string: 'Y' to 'X' ("YYY" to "XYY")

    Parameters:

    - `pattern`: Pattern or string to look for.
    - `replacement`: A string of replacements.
    """
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def resolve(self, column):
        return column.str.replace(self.pattern, self.replacement, n=1)


class StrReplaceAll(StrTransformer):
    """
    Replace all ocurrences of matched patterns in a string: 'Y' to 'X' ("YYY" to "XXX")

    Parameters:

    - `pattern`: Pattern or string to look for.
    - `replacement`: A string of replacements.
    """
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def resolve(self, column):
        return column.str.replace(self.pattern, self.replacement, n=-1)


class StrPad(StrTransformer):
    """
    Pad a string: 'Y' to 4 chars, left and '0' ("Y" to "000Y")

    Parameters:

    - `width`: Minimum width of padded strings.
    - `side`: Side on which padding character is added (left, right or both).
    - `pad`: Single padding character (default is a space).
    """
    def __init__(self, width, side="left", pad=" "):
        self.width = width
        self.side = side
        self.pad = pad

    def resolve(self, column):
        return column.str.pad(self.width, side=self.side, fillchar=self.pad)
