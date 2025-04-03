def kebab_to_pascal(string: str) -> str:
    words = string.split("-")
    return "".join([word[0].upper() + word[1:].lower() for word in words])

def kebab_to_camel(string: str) -> str:
    string = kebab_to_pascal(string)
    return string[0].lower() + string[1:]

def kebab_to_snake(string: str) -> str:
    return string.replace("-", "_")

def space(num: int) -> str:
    return " " * num

def tab(num: int=1, tab_width: int=4) -> str:
    return " " * num * tab_width

def log_created(type: str, path: str, with_files: list[str]) -> None:
    print(f"{type[0].upper() + type[1:].lower()} '{path}' was created with {"file" if len(with_files) == 1 else "files"} '{"', '".join(with_files)}'.")

SEP = "=================================================="