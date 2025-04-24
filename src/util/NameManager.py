from typing import Literal


class NameManager:
    __instance: "NameManager" = None
    camel: str = "camel"
    pascal: str = "pascal"
    upper: str = "upper"
    snake: str = "snake"
    kebab: str = "kebab"

    def __init__(self) -> None:
        if NameManager.__instance is not None:
            raise RuntimeError("Use NameManager.instance() instead")

    @classmethod
    def instance(cls: type["NameManager"]) -> "NameManager":
        if cls.__instance is None:
            cls.__instance = NameManager()
        return cls.__instance

    def __split_at_upper(string: str) -> list[str]:
        words = []
        start = 0
        string = string.lstrip("_")

        for i in range(1, len(string)):
            curr = string[i]
            last = string[i - 1]
            if i+1 < len(string):
                next = string[i+1]
            else: 
                next = None
            
            if curr.isdigit() and not last.isdigit():
                words.append(string[start:i])
                start = i
            elif curr.isupper():
                if last.islower():
                    words.append(string[start:i])
                    start = i
                elif next is not None and next.islower():
                    words.append(string[start:i])
                    start = i
                elif next is not None and next.isupper():
                    continue
        words.append(string[start:])
        return words

    def __to_spaced(
        self,
        string: str,
        case_in: Literal["camel", "pascal", "upper", "snake", "kebab"]
    ) -> str:
        if case_in == self.camel:
            return self.__split_at_upper(string)
        elif case_in == self.kebab:
            return string.lower().split("-")
        elif case_in == self.pascal:
            return self.__split_at_upper(string)
        elif case_in == self.snake:
            return string.lower().split("_")
        elif case_in == self.upper:
            return string.lower().split("_")
        else:
            raise ValueError(f"Unknown naming convention '{case_in}'")
    def __spaced_to(
            self,
            words: list[str],
            case_out: Literal["camel", "pascal", "upper", "snake", "kebab"]
    ) -> str:
        if case_out == self.camel:
            return words[0].lower() + "".join(word.capitalize() for word in words[1:])
        elif case_out == self.pascal:
            return "".join([word.capitalize() for word in words])
        elif case_out == self.upper:
            return "_".join([word.upper() for word in words])
        elif case_out == self.snake:
            return "_".join([word.lower() for word in words])
        elif case_out == self.kebab:
            return "-".join([word.lower() for word in words])
        else:
            raise ValueError(f"Unknown naming convention '{case_out}'")
        
    def switch(
        self,
        string: str,
        case_in: Literal["camel", "pascal", "upper", "snake", "kebab"],
        case_out: Literal["camel", "pascal", "upper", "snake", "kebab"]
    ) -> str:
        return self.__spaced_to(self.__to_spaced(string, case_in), case_out)
