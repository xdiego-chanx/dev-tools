from dataclasses import dataclass

@dataclass
class TemplateBase:
    filename: str
    contents: list[str]