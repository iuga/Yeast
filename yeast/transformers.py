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
    Convert case of a string to Upper case: ("Yeast" to "YEAST")
    """
    def resolve(self, column):
        return column.str.upper()


class StrToLower(StrTransformer):
    """
    Convert case of a string to Lower case:  ("Yeast" to "yeast")
    """
    def resolve(self, column):
        return column.str.lower()


class StrToSentence(StrTransformer):
    """
    Convert case of a string to Sentence Case: ("yeast help" to "Yeast Help")
    """
    def resolve(self, column):
        return column.str.title()


class StrTrim(StrTransformer):
    """
    Convert removing whitespaces from start and end of string:  (" Yeast " to "Yeast")
    """
    def resolve(self, column):
        return column.str.strip()


class StrReplace(StrTransformer):
    """
    Replace first ocurrence of matched patterns in a string: 'Y' to 'X' ("YYY" to "XYY")
    """
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def resolve(self, column):
        return column.str.replace(self.pattern, self.replacement, n=1)


class StrReplaceAll(StrTransformer):
    """
    Replace all ocurrences of matched patterns in a string: 'Y' to 'X' ("YYY" to "XXX")
    """
    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def resolve(self, column):
        return column.str.replace(self.pattern, self.replacement, n=-1)
