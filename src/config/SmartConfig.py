from dataclasses import dataclass

@dataclass
class SmartConfig:
    quotes: str
    arrow_function_args: tuple[str, str]
    semicolon: str