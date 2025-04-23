from dataclasses import dataclass
from typing import Literal

@dataclass
class ConfigProfile:
    quotes: Literal["single", "double"]
    indent: Literal["tab", "space"]
    bracket_spacing: Literal["tight", "space", "newline"]
    arrow_function_args: Literal["parentheses", "omit"]
    eol: Literal["cr", "lf", "crlf"]
    tab_width: int
    semicolon: bool
    trailing_comma: bool
    spaced_objects: bool