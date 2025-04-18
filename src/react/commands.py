import os
from . import templates
from .. import lib
from ..lib import console

def view(path: str, css: bool=False, layout: bool=False, tsx: bool=False, flat: bool = False) -> None:
    try:
        name, path = lib.split_path(path, flat)

        if not os.path.exists(path):
            os.makedirs(path)
        
        lang = "tsx" if tsx else "jsx"
        files = [templates.react_view(name, lang, css)]

        if css:
            files.append(templates.react_css(name))

        if layout: 
            files.append(templates.react_layout(name, lang))
        
        lib.write_files(files, path)

        console.log_created("view", path, [file["name"] for file in files])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")

def component(
        path: str,
        css: bool = False,
        tsx: bool = False,
        flat: bool = False
        ) -> None:
    try:
        name, path = lib.split_path(path, flat)

        if not os.path.exists(path):
            os.makedirs(path)
        
        lang = "tsx" if tsx else "jsx"
        files = [templates.react_component(name, lang, css)]

        if css:
            files.append(templates.react_css(name))

        lib.write_files(files, path)

        console.log_created("module", path, [file["name"] for file in files])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")