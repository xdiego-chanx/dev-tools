import argparse
import os
from . import lib
from . import templates

def react_module(name, path, lang="js", nojsx= False):
    path = os.path.abspath(path)
    if lang not in ["js", "ts"]:
        raise TypeError("Language mode for React JSX components should be either 'js' or 'ts'")
    module_path = os.path.join(path, name)
    lang = lang if nojsx else lang + "x"
    if not os.path.exists(module_path):
        os.makedirs(module_path, exist_ok=True)
    module_files = templates.react_module(name, lang)

    for filename, contents in module_files.items():
        with open(os.path.join(module_path, filename), "w") as file:
            file.write("\n".join(contents))
    print(f"Module {module_path} was created successfully.")

def aspnet_module(name, path):
    path = os.path.abspath(path)
    module_path = os.path.join(path, name)
    if not os.path.exists(module_path):
        os.makedirs(module_path, exist_ok=True)
    namespace = lib.resolve_csharp_namespace(module_path)
    s_name = lib.singularize_name(name)
    module_files = templates.aspnet_module(namespace, s_name)

    for filename, contents in module_files.items():
        with open(os.path.join(module_path, filename + ".cs"), "w") as file:
            file.write("\n".join(contents))
    print(f"Module {module_path} was created successfully.")

def nestjs_module(name, path, lang="ts", root=False):
    path = os.path.abspath(path)
    module_path = path if root else os.path.join(path, name)
    if not os.path.exists(module_path):
        os.makedirs(module_path, exist_ok=True)
    module_files = templates.nestjs_module(name, lang)
    for filename, contents in module_files.items():
        with open(os.path.join(module_path, filename), "w") as file:
            file.write("\n".join(contents))
    print(f"Module {module_path} was created successfully.")

def main():
    parser = argparse.ArgumentParser(description="CLI for common utilities")
    subparsers = parser.add_subparsers(dest="context", required=True, help="aspnet: Commands for ASP.NET utilities.\nreact: Command for react utilities.")

    # aspnet
    aspnet_parser = subparsers.add_parser("aspnet")
    aspnet_subparsers = aspnet_parser.add_subparsers(dest="command", required=True)

    # aspnet new
    aspnet_new_parser = aspnet_subparsers.add_parser("new")
    aspnet_new_subparsers = aspnet_new_parser.add_subparsers(dest="subcommand", required=True)
    
    #aspnet new module
    aspnet_new_module_parser = aspnet_new_subparsers.add_parser("module", help="Create a new ASP.NET module")
    aspnet_new_module_parser.add_argument("name", help="Module name")
    aspnet_new_module_parser.add_argument("path", nargs="?", help="Path where the module should be created", default=".")

    # react
    react_parser = subparsers.add_parser("react")
    react_subparsers = react_parser.add_subparsers(dest="command", required=True)

    # react new
    react_new_parser = react_subparsers.add_parser("new")
    react_new_subparsers = react_new_parser.add_subparsers(dest="subcommand", required=True)

    # react new module
    react_new_module_parser = react_new_subparsers.add_parser("module", help="Create a new React module")
    react_new_module_parser.add_argument("name", help="Module name")
    react_new_module_parser.add_argument("path", nargs="?", help="Path where the module should be created", default=".")
    react_new_module_parser.add_argument("--lang", choices=["js", "ts"], help="Sets the language for the files created", default="js")
    react_new_module_parser.add_argument("--no-jsx", action="store_true", help="Use .js and .ts file extensions instead of .jsx and .tsx")

    # nest
    nestjs_parser = subparsers.add_parser("nest")
    nestjs_subparsers = nestjs_parser.add_subparsers(dest="command", required=True)

    # nest new
    nestjs_new_parser = nestjs_subparsers.add_parser("new")
    nestjs_new_subparsers = nestjs_new_parser.add_subparsers(dest="subcommand", required=True)

    # nest new module
    nestjs_new_module_parser = nestjs_new_subparsers.add_parser("module", help="Create a new NestJS module")
    nestjs_new_module_parser.add_argument("name", help="Module name")
    nestjs_new_module_parser.add_argument("path", nargs="?", help="Path where the module should be created", default="./src")
    nestjs_new_module_parser.add_argument("--lang", choices=["js", "ts"], help="Sets the language for the files created", default="ts")
    nestjs_new_module_parser.add_argument("--root", action="store_true", help="Make the NestJS module on the path specified, without creating a folder.")
    
    args = parser.parse_args()

    if args.context == "aspnet": # aspnet
        if args.command == "new": # aspnet new
            if args.subcommand == "module": # aspnet new module
                aspnet_module(args.name, args.path)
    elif args.context == "react": # react
        if args.command == "new":   # react new
            if args.subcommand == "module": # react new module
                react_module(args.name, args.path, args.lang, args.no_jsx)
    elif args.context == "nest": # nest
        if args.command == "new": # nest new
            if args.subcommand == "module": # nest new module
                nestjs_module(args.name, args.path, args.lang, args.root)

if __name__ == "__main__":
    main()