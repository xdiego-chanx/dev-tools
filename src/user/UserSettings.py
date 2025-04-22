from argparse import ArgumentError
from math import isnan

class UserSettings:
    __quotes="double"
    __indent="space"
    __tab_width=4
    __semicolon=True
    __opening_brace_style="space"

    def get_quotes(self) -> str:
        return self.__quotes
    
    def set_quotes(self, quotes: str) -> None:
        if quotes not in ["single", "double", "backtick"]:
            raise ArgumentError("'Quotes' attribute must be either 'single', 'double' or 'backtick'")
        self.__quotes = quotes
        return
    
    def get_indent(self) -> str:
        return self.__indent
    
    def set_indent(self, indent: str) -> None:
        if indent not in ["tab", "space"]:
            raise ArgumentError("'Indent' attribute must be either 'tab' or 'space'.")
        self.__indent = indent
        return
    
    def get_tab_width(self) -> int:
        return self.__tab_width
    
    def set_tab_width(self, tab_width: str) -> None:
        if isnan(int(tab_width)) or tab_width < 0:
            raise ArgumentError("'Indent' attribute must be a positive integer.")
        else:
            self.__tab_width = int(tab_width)
        return
    
    def get_semicolon(self) -> bool:
        return self.__semicolon
    
    def set_semicolon(self, semicolon: bool) -> None:
        self.__semicolon = semicolon

    def get_opening_brace_style(self) -> str:
        return self.__opening_brace_style
    
    def set_opening_brace_style(self, opening_brace_style: str) -> None:
        if opening_brace_style not in ["collapsed", "space", "newline"]:
            raise ArgumentError("'Opening Brace Style' attribute must be either 'collapsed', 'space', or 'newline'")
        self.__opening_brace_style = opening_brace_style
        return
     