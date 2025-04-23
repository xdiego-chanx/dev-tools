from dataclasses import dataclass
from typing import Literal

@dataclass
class ConfigProfile:
    quotes: Literal["smart", "single", "double"]
    indent: Literal["tab", "space"]
    bracket_spacing: Literal["tight", "space", "newline"]
    eol: Literal["cr", "lf", "crlf"]
    tab_width: int
    semicolon: Literal["smart", "use", "avoid"]
    trailing_comma: bool
    spaced_objects: bool 

    @classmethod
    def default(cls: type["ConfigProfile"]) -> "ConfigProfile":
        return cls(
            quotes="double",
            indent="space",
            bracket_spacing="space",
            eol="crlf",
            tab_width=4,
            semicolon=True,
            trailing_comma=False,
            spaced_objects=True
        )