from dataclasses import dataclass
from typing import Literal

@dataclass
class TemplateBase:
    filename: str
    mode: Literal["create", "update"]
    contents: list[str]