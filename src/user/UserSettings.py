class UserSettings:


    def __init__(self):
        return
    
class Nest:
    __quotes="double"
    __indent="space"
    
    def set_quotes(self, quotes: str) -> None:
        if quotes not in ["single", "double", "backtick"]:
            raise ValueError("'Quotes' attribute must be either 'single', 'double' or 'backtick'")
        self.__quotes = quotes
        return
    
    def get_quotes(self) -> str:
        return self.__quotes
    
    def set_indent(self, indent: str) -> None:
        if indent not in ["tab", "space"]:
            raise ValueError("'Indent' attribute must be either 'tab' or 'space'.")
