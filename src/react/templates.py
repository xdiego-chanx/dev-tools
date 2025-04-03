from .. import lib

def react_component(name: str, lang: str, css: bool) -> dict[str, str | list[str]]:
    view = {
        "name": f"{lib.kebab_to_pascal(name)}.{lang}",
        "content": [
            f"export default function {lib.kebab_to_pascal(name)}(){": React.JSX.Element" if lang == "ts" else ""} {{",
            f"{lib.tab()}return (",
            f"{lib.tab(2)}<>",
            lib.tab(3),
            f"{lib.tab(2)}</>",
            f"{lib.tab()});",
            "}",
        ],
    }

    if css:
            view["content"] = [f"import styles from \"./{name}.module.css\";", ""] + view["content"]
    return view

def react_view(name: str, lang: str, css: bool) -> dict[str, str | list[str]]:
    view = {
        "name": f"page.{lang}",
        "content": [
            f"export default function {lib.kebab_to_pascal(name)}View(){": React.JSX.Element" if lang == "ts" else ""} {{",
            f"{lib.tab()}return (",
            f"{lib.tab(2)}<>",
            lib.tab(2),
            f"{lib.tab(2)}</>",
            f"{lib.tab()});",
            "}",
        ],
    }

    if css:
        view["content"] = [f"import styles from \"./{name}.module.css\";", ""] + view["content"]
    return view


def react_layout(name: str, lang: str) -> dict[str, str | list[str]]:
    return {
        "name": f"layout.{lang}",
        "content": [
            f"export default function {lib.kebab_to_pascal(name)}Layout(){": React.JSX.Element" if lang == "ts" else ""} {{",
            f"{lib.tab()}return (",
            f"{lib.tab(2)}<>",
            lib.tab(2),
            f"{lib.tab(2)}</>",
            f"{lib.tab()});",
            "}",
        ],
    }


def react_css(name: str) -> dict[str, str | list[str]]:
    return {
        "name": f"{name}.module.css",
        "content": [f"/* CSS module file for {lib.kebab_to_pascal(name)} */"]
    }
