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

    for i, char in enumerate(string):
        if i > 0 and char.isupper() or char.isnumeric():
            words.append(string[start:i])
            start = i

    words.append(string[start:])
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

def log_created(type: str, path: str, with_files: list[str]) -> None:
    cap_type = type[0].upper() + type[1:].lower()
    conj_files = "file" if len(with_files) == 1 else "files"
    print(
        f"{cap_type} '{path}' was created with {conj_files} '{"', '".join(with_files)}'."
    )


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


def modify_module(path: str, add: str) -> None:
    pascal_add = switch_naming_conv(add, kebab, pascal)
    array_names = {"controller": "controllers", "service": "providers"}
    decl_found = False
    module_index = -1
    file, path = split_path(path)
    name, _ = os.path.splitext(file)

    pascal_name = switch_naming_conv(name, kebab, pascal)

    with open(path, "r+", encoding="utf-8") as module:
        lines = module.readlines()

        for i, line in enumerate(lines):
            if line.strip() == "@Module({":
                module_index = i
            if line.strip().startswith(array_names[add]):
                decl_found = True
                lines[i] = (
                    line.rstrip().rstrip("]") + f", {pascal_name}{pascal_add}],\n"
                )
                break

        if not decl_found:
            lines.insert(
                module_index + 1,
                f"{TAB}{array_names[add]}: [{pascal_name}{pascal_add}],\n",
            )

        import_stmt = f'import {{ {pascal_name}{pascal_add} }} from "./{name}.{add}";\n'

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
        print("Finding node...")
        node_v = subprocess.run(
            ["node", "--version"], capture_output=True, text=True
        ).stdout
        return node_v.lstrip("v")
    except FileNotFoundError:
        return False


def find_npm() -> tuple[str] | bool:
    try:
        print("Finding npm...")
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

warn = lambda string: print(f"\033[93m{string}\033[0m")
error = lambda string: print(f"\033[31m{string}\033[0m")

SEP = "=" * 100
TAB = "    "
