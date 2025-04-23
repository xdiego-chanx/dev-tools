from dataclasses import dataclass

@dataclass
class TemplateBase:
    name: str
    lang: str
    contents: list[str]