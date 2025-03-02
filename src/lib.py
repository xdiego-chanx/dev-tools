import os

def resolve_csharp_namespace(path, original_path=None):
    path = os.path.abspath(path)

    if original_path is None:
        original_path = path
    
    path_files = [item for item in os.scandir(path) if item.is_file()]

    for file in path_files: 
        if os.path.splitext(file.name)[1] in [".sln", ".csproj"]:
            project_root = path
            namespace_root = os.path.basename(project_root)
            rel_path = os.path.relpath(original_path, project_root)
            
            namespace = (namespace_root + "." + rel_path.replace(os.sep, ".")).replace("..", ".")
            return namespace
    if(path == os.path.dirname(path)):
        print("C# project root not found.")
        return None
    else:
        return resolve_csharp_namespace(os.path.dirname(path), original_path)
    
def singularize_name(name):
    irregulars = {
        "beliefs": "belief",
        "chefs": "chef",
        "feet": "foot",
        "children": "child",
        "fish": "fish",
        "sheep": "sheep",
        "oxen": "ox"
    }
    if name in irregulars.keys():
        return irregulars[name]
    if name.endswith("ies") and len(name) > 3:
        return name.removesuffix("ies") + "y"
    if name.endswith("ves"):
        return name.removesuffix("ves") + "f"
    if name.endswith("es"):
        return name.removesuffix("s")
    if name.endswith("s") and not name.endswith("ss"):
        return name.removesuffix("s")
    return name

def capitalize_name(name):
    return name[0].upper() + name[1:]

def space(qty):
    return " " * qty