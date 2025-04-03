import os
from . import templates
from .. import lib

def view(name: str, path: str=".", css: bool=False, layout: bool=False, tsx: bool=False) -> None:
    path = os.path.abspath(path)
    view_dir = os.path.join(path, name)

    if not os.path.exists(view_dir):
        os.makedirs(view_dir)
    
    lang = "tsx" if tsx else "jsx"
    files = [templates.react_view(name, lang, css)]

    if css:
        files.append(templates.react_css(name))

    if layout: 
        files.append(templates.react_layout(name, lang))
    
    for template in files:
        with open(os.path.join(view_dir, template["name"]), "w", encoding="utf-8") as file:
            file.write("\n".join([line for line in template["content"]]))
    
    lib.log_created("view", view_dir, [file["name"] for file in files])

def component(name: str, path: str=".", css: bool=False, new_dir: bool=False, tsx: bool=False) -> None:
    path = os.path.abspath(path)
    view_dir = os.path.join(path, name) if new_dir else path

    if not os.path.exists(view_dir):
        os.makedirs(view_dir)
    
    lang = "tsx" if tsx else "jsx"
    files = [templates.react_component(name, lang, css)]

    if css:
        files.append(templates.react_css(name))
    
    for template in files:
        with open(os.path.join(view_dir, template["name"]), "w", encoding="utf-8") as file:
            file.write("\n".join([line for line in template["content"]]))

    lib.log_created("module", path, [file["name"] for file in files])