import os
from . import templates
from .. import lib
import subprocess
import json


def feature(
    name: str,
    path: str = ".",
    orm: str = "tyeorm",
    use_uuid: bool = True,
    js: bool = False,
    no_entity: bool = True,
    no_controller: bool = False,
    no_service: bool = False,
) -> None:
    path = os.path.abspath(path)
    ft_dir = os.path.join(path, name)

    if not os.path.exists(ft_dir):
        os.makedirs(ft_dir)

    lang = "js" if js else "ts"
    files = [templates.nest_module(name, lang, not no_controller, not no_service)]

    if not no_controller:
        files.append(templates.nest_controller(name, lang))

    if not no_entity:
        files.append(templates.nest_entity(name, lang, orm, use_uuid))

    if not no_service:
        files.append(templates.nest_service(name, lang))

    for template in files:
        with open(
            os.path.join(ft_dir, template["name"]), "w", encoding="utf-8"
        ) as file:
            file.write("\n".join(template["content"]))

    lib.log_created("feature", ft_dir, [file["name"] for file in files])


def module(name: str, path: str = ".", js: bool = False):
    path = os.path.abspath(path)
    module_dir = os.path.join(path, name)

    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    lang = "js" if js else "ts"
    template = templates.nest_module(name, lang, controller=False, service=False)

    with open(
        os.path.join(module_dir, template["name"]), "w", encoding="utf-8"
    ) as file:
        file.write("\n".join(template["content"]))

    lib.log_created("module", module_dir, [template["name"]])


def controller(name: str, path: str = ".", js: bool = False):
    path = os.path.abspath(path)
    ctrl_dir = os.path.join(path, name)

    lang = "js" if js else "ts"

    if not os.path.exists(os.path.join(ctrl_dir, f"{name}.module.{lang}")):
        raise ModuleNotFoundError(
            f"A controller cannot be attached to non-existent module '{name}.module.{lang}'."
        )

    template = templates.nest_controller(name, lang)

    with open(os.path.join(ctrl_dir, template["name"]), "w", encoding="utf-8") as file:
        file.write("\n".join(template["content"]))

    with open(
        os.path.join(ctrl_dir, f"{name}.module.{lang}"), "r+", encoding="utf-8"
    ) as module:
        pascal_name = lib.kebab_to_pascal(name)
        lines = module.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith("controllers"):
                lines[i] = line.rstrip().rstrip("]") + f", {pascal_name}Controller],\n"
                break
        else:
            for i, line in enumerate(lines):
                if line.strip() == "@Module({":
                    lines.insert(
                        i + 1, f"{lib.tab()}controllers: [{pascal_name}Controller],\n"
                    )
                    break

        import_stmt = (
            f'import {{ {pascal_name}Controller }} from "./{name}.controller";\n'
        )
        if import_stmt not in lines:
            lines.insert(1, import_stmt)

        module.seek(0)
        module.writelines(lines)
        module.truncate()

    lib.log_created("controller", ctrl_dir, [template["name"]])


def service(name: str, path: str = ".", js: bool = False):
    path = os.path.abspath(path)
    service_dir = os.path.join(path, name)

    lang = "js" if js else "ts"

    if not os.path.exists(os.path.join(service_dir, f"{name}.module.{lang}")):
        raise ModuleNotFoundError(
            f"A service cannot be attached to non-existent module '{name}.module.{lang}'."
        )

    template = templates.nest_service(name, lang)

    with open(
        os.path.join(service_dir, template["name"]), "w", encoding="utf-8"
    ) as file:
        file.write("\n".join(template["content"]))

    with open(
        os.path.join(service_dir, f"{name}.module.{lang}"), "r+", encoding="utf-8"
    ) as module:
        pascal_name = lib.kebab_to_pascal(name)
        lines = module.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith("providers"):
                lines[i] = line.rstrip().rstrip("]") + f", {pascal_name}Service],\n"
                break
        else:
            for i, line in enumerate(lines):
                if line.strip() == "@Module({":
                    lines.insert(
                        i + 1, f"{lib.tab()}providers: [{pascal_name}Service],\n"
                    )
                    break

        import_stmt = f'import {{ {pascal_name}Service }} from "./{name}.service";\n'
        if import_stmt not in lines:
            lines.insert(1, import_stmt)

        module.seek(0)
        module.writelines(lines)
        module.truncate()

    lib.log_created("service", service_dir, [template["name"]])


def entity(
    name: str,
    path: str = ".",
    js: bool = False,
    orm: str = "tyeorm",
    use_uuid: bool = True,
):
    path = os.path.abspath(path)
    entity_dir = os.path.join(path, name)
    pascal_name = lib.kebab_to_pascal(name)

    lang = "js" if js else "ts"

    if not os.path.exists(os.path.join(entity_dir)):
        print(
            f"Consider making a module '{name}.module.{lang}' at '{entity_dir}' before using entity '{pascal_name}'."
        )
        os.makedirs(entity_dir)

    template = templates.nest_entity(name, lang, orm, use_uuid)

    with open(
        os.path.join(entity_dir, template["name"]), "w", encoding="utf-8"
    ) as file:
        file.write("\n".join(template["content"]))

    lib.log_created("entity", entity_dir, [template["name"]])


def microservice(name: str, path: str = ".", js: bool = False):
    path = os.path.abspath(path)
    ms_dir = os.path.join(path, name)
    lang = "js" if js else "ts"

    if not os.path.exists(ms_dir):
        os.makedirs(ms_dir)
    else:
        if os.path.isdir(ms_dir) and len(os.listdir(ms_dir)) > 0:
            print("Creating projects in non-empty directories is not recommended. Stopping...")
            return

    try:
        print("Finding node...")
        node_v = subprocess.run(["node", "--version"], cwd=ms_dir, capture_output=True, text=True).stdout;
        print(f"Node.js {node_v}")
    except FileNotFoundError:
        print("Node.js was not found in this machine.")
        return
    
    try:
        npm_v = subprocess.run(["npm", "--version"], cwd=ms_dir, capture_output=True, text=True).stdout
        npm = "npm"
        print(f"{npm} {npm_v}")
        
    except FileNotFoundError:
        try:
            npm_v = subprocess.run(["npm.cmd", "--version"], cwd=ms_dir, capture_output=True, text=True).stdout
            npm = "npm.cmd"
            print(f"{npm} {npm_v}")
        except FileNotFoundError:
            print("npm was not found in this machine.")
            return
        
    print(lib.SEP)
    print("Creating Node.js project...")
    subprocess.run([npm, "init", "-y"], cwd=ms_dir, capture_output=True, text=True)
    print("Node.js project created successfully!")
    
    print(lib.SEP)
    print("Modifying root-level files...")
    with open(os.path.join(ms_dir, "package.json"), "r+", encoding="utf-8") as json_file:
        package_json = json.load(json_file)
        
        package_json["type"] = "module"
        package_json["main"] = f"src/main.{lang}"

        json_file.seek(0)
        json.dump(package_json, json_file, indent=4)
        json_file.truncate()

    subprocess.run(
        [
            npm,
            "i",
            "typescript",
            "tsc",
            "@nestjs/core",
            "@nestjs/common",
            "@nestjs/config",
            "@nestjs/platform-express",
            "@nestjs/microservices",
            "reflect-metadata",
            "class-validator",
            "class-transformer",
        ],
        cwd=ms_dir, capture_output=True, text=True
    )
    subprocess.run([npm, "i", "-D", "@types/node"], cwd=ms_dir, capture_output=True, text=True)

    src = os.path.join(ms_dir, "src")
    os.mkdir(src)

    src_files = [
        templates.nest_main(lang),
        templates.nest_module("app", lang, True, True),
        templates.nest_controller("app", lang),
        templates.nest_service("app", lang),
    ]

    with open(os.path.join(ms_dir, ".gitignore"), "w", encoding="utf-8") as gitignore:
        gitignore.write("\n".join(templates.nest_gitignore()))

    with open(os.path.join(ms_dir, "tsconfig.json"), "w", encoding="utf-8") as tsconfig:
        tsconfig.write(templates.nest_tsconfig())

    with open(os.path.join(ms_dir, "Dockerfile"), "w", encoding="utf-8") as dockerfile:
        dockerfile.write("\n".join(templates.nest_dockerfile()))
    
    for src_file in src_files:
        with open(os.path.join(src, src_file["name"]), "w", encoding="utf-8") as file:
            file.write("\n".join(src_file["content"]))
