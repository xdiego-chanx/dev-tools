import json
import os
import subprocess
from typing import Any

camel = "camel case"
pascal = "pascal case"
upper = "upper case"
snake = "snake case"
kebab = "kebab case"


def switch_naming_conv(string: str, from_f: str, to_f: str) -> str:
    spaced = []
    if from_f == camel:
        spaced = camel_to_spaced(string)
    elif from_f == pascal:
        spaced = pascal_to_spaced(string)
    elif from_f == upper:
        spaced = upper_to_spaced(string)
    elif from_f == snake:
        spaced = snake_to_spaced(string)
    elif from_f == kebab:
        spaced = kebab_to_spaced(string)
    else:
        raise ValueError("Naming convention not accepted.")
    if to_f == camel:
        return spaced_to_camel(spaced)
    elif to_f == pascal:
        return spaced_to_pascal(spaced)
    elif to_f == upper:
        return spaced_to_upper(spaced)
    elif to_f == snake:
        return spaced_to_snake(spaced)
    elif to_f == kebab:
        return spaced_to_kebab(spaced)
    else:
        raise ValueError("Naming convention not accepted.")

def split_at_upper(string: str) -> list[str]:
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
    print(words)
    return words


camel_to_spaced = lambda string: split_at_upper(string)

pascal_to_spaced = lambda string: split_at_upper(string)

upper_to_spaced = lambda string: string.lower().split("_")

snake_to_spaced = lambda string: string.lower().split("_")

kebab_to_spaced = lambda string: string.lower().split("-")

spaced_to_camel = lambda array: array[0].lower() + "".join(word.capitalize() for word in array[1:])

spaced_to_pascal = lambda array: "".join(word.capitalize() for word in array)

spaced_to_upper = lambda array: "_".join(array).upper()

spaced_to_snake = lambda array: "_".join(array).lower()

spaced_to_kebab = lambda array: "-".join(array).lower()

def split_path(path_input: str, flat: bool = False) -> tuple[str]:
    name = os.path.basename(path_input)
    path = (
        os.path.abspath(path_input)
        if not flat
        else os.path.abspath(os.path.dirname(path_input))
    )
    return (name, path)


def write_files(templates: dict[str, str | list[str]], path: str) -> None:
    for template in templates:
        with open(os.path.join(path, template["name"]), "w", encoding="utf-8") as file:
            file.write("\n".join(template["content"]))


def modify_module(module_path: str, ft_name: str, filetype: str) -> None:
    class_name = f"{switch_naming_conv(ft_name, kebab, pascal)}{switch_naming_conv(filetype, kebab, pascal)}"
    import_path = f"./{ft_name}.{filetype}"
    module_index = -1
    decl_array_found = False

    array_names = {
        "controller": "controllers",
        "service": "providers"
    }

    with open(module_path, "r+", encoding="utf-8") as module:
        lines = module.readlines()

        for i, line in enumerate(lines):
            if line.strip() == "@Module({":
                module_index = i
            if line.strip().startswith(array_names[filetype]):
                decl_array_found = True
                lines[i] = (
                    line.rstrip().rstrip(",").rstrip("]") + f", {class_name}],\n")
                break
        if not decl_array_found:
            lines.insert(
                module_index + 1,
                f"{TAB}{array_names[filetype]}: [{class_name}],\n",
            )

        import_stmt = f"import {{ {class_name} }} from \"{import_path}\";\n"

        if import_stmt not in lines:
            lines.insert(1, import_stmt)

        module.seek(0)
        module.writelines(lines)
        module.truncate()


def read_package_json(at: str) -> dict[str, Any]:
    with open(os.path.join(at, "package.json"), "r+", encoding="utf-8") as json_file:
        package_json = json.load(json_file)
    return package_json


def rewrite_package_json(at: str, package_json: dict[str | Any]) -> None:
    with open(os.path.join(at, "package.json"), "r+", encoding="utf-8") as json_file:
        json_file.seek(0)
        json.dump(package_json, json_file, indent=4)
        json_file.truncate()


def find_node() -> str | bool:
    try:
        node_v = subprocess.run(
            ["node", "--version"], capture_output=True, text=True
        ).stdout
        return node_v.lstrip("v")
    except FileNotFoundError:
        return False
    
def find_bun() -> str | bool:
    try: 
        bun_v = subprocess.run(
            ["bun", "--version"], capture_output=True, text=True
        ).stdout
        return bun_v
    except FileNotFoundError:
        return False

def find_npm() -> tuple[str] | bool:
    try:
        npm_v = subprocess.run(
            ["npm", "--version"], capture_output=True, text=True
        ).stdout
        return ("npm", npm_v)

    except FileNotFoundError:
        try:
            npm_v = subprocess.run(
                ["npm.cmd", "--version"], capture_output=True, text=True
            ).stdout
            return ("npm.cmd", npm_v)

        except FileNotFoundError:
            return False

class Console:
    __WHITE = "\033[97m"
    __BLUE = "\033[96m"
    __YELLOW = "\033[93m"
    __RED = "\033[31m"
    __GREEN = "\033[92m"
    __STOP = "\033[0m"

    def log_created(self, type: str, path: str, with_files: list[str]) -> None:
        cap_type = type[0].upper() + type[1:].lower()
        conj_files = "file" if len(with_files) == 1 else "files"
        print(
            f"{self.__WHITE}{cap_type} '{path}' was created with {conj_files} '{"', '".join(with_files)}'.{self.__STOP}"
        )

    def log(self, x: str) -> None:
        print(f"{self.__WHITE}{x}{self.__STOP}")

    def info(self, x: str) -> None:
        print(f"{self.__BLUE}{x}{self.__STOP}")

    def debug(self, x: str) -> None:
        print(f"{self.__GREEN}{x}{self.__STOP}")

    def warn(self, x: str) -> None:
        print(f"{self.__YELLOW}{x}{self.__STOP}")

    def error(self, x: str) -> None:
        print(f"{self.__RED}{x}{self.__STOP}")


console = Console()

SEP = "=" * 75
TAB = "    "
