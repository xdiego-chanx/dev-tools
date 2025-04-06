from .. import lib

def react_component(name: str, lang: str, css: bool) -> dict[str, str | list[str]]:
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)
    view = {
        "name": f"{pascal_name}.{lang}",
        "content": [
            f"export default function {pascal_name}(){": React.JSX.Element" if lang == "ts" else ""} {{",
            f"{lib.TAB}return (",
            f"{lib.TAB * 2}<>",
            lib.TAB * 3,
            f"{lib.TAB * 2}</>",
            f"{lib.TAB});",
            "}",
        ],
    }

    if css:
            view["content"] = [f"import styles from \"./{name}.module.css\";", ""] + view["content"]
    return view

def react_view(name: str, lang: str, css: bool) -> dict[str, str | list[str]]:
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)
    view = {
        "name": f"page.{lang}",
        "content": [
            f"export default function {pascal_name}View(){": React.JSX.Element" if lang == "ts" else ""} {{",
            f"{lib.TAB}return (",
            f"{lib.TAB * 2}<>",
            lib.TAB * 2,
            f"{lib.TAB * 2}</>",
            f"{lib.TAB});",
            "}",
        ],
    }

    if css:
        view["content"] = [f"import styles from \"./{name}.module.css\";", ""] + view["content"]
    return view


def react_layout(name: str, lang: str) -> dict[str, str | list[str]]:
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)
    return {
        "name": f"layout.{lang}",
        "content": [
            f"export default function {pascal_name}Layout(){": React.JSX.Element" if lang == "ts" else ""} {{",
            f"{lib.TAB}return (",
            f"{lib.TAB * 2}<>",
            lib.TAB * 2,
            f"{lib.TAB * 2}</>",
            f"{lib.TAB});",
            "}",
        ],
    }


def react_css(name: str) -> dict[str, str | list[str]]:
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)
    return {
        "name": f"{name}.module.css",
        "content": [f"/* CSS module file for {pascal_name} */"]
    }
