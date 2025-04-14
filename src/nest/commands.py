import os
from . import templates
from .. import lib
from ..lib import console
import subprocess
from glob import glob


def feature(
    path: str,
    orm: str = "tyeorm",
    use_uuid: bool = True,
    js: bool = False,
    no_entity: bool = True,
    no_controller: bool = False,
    no_service: bool = False,
    flat: bool = False
) -> None:
    try:
        name, path = lib.split_path(path, flat)

        if not os.path.exists(path):
            os.makedirs(path)

        lang = "js" if js else "ts"

        files = [templates.nest_module(name, lang, not no_controller, not no_service)]

        if not no_controller:
            files.append(templates.nest_controller(name, lang))

        if not no_entity:
            files.append(templates.nest_entity(name, lang, orm, use_uuid))

        if not no_service:
            files.append(templates.nest_service(name, lang))

        lib.write_files(files, path)

        console.log_created("feature", path, [file["name"] for file in files])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")


def module(path: str, js: bool = False, flat: bool = False) -> None:
    try:
        name, path = lib.split_path(path, flat)
        filetype = "module"

        if not os.path.exists(path):
            os.makedirs(path)

        lang = "js" if js else "ts"

        template = templates.nest_module(name, lang, controller=False, service=False)
        lib.write_files([template], path)

        console.log_created(filetype, path, [template["name"]])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")


def controller(path: str, js: bool = False, flat: bool = False) -> None:
    try:
        name, path = lib.split_path(path, flat)
        filetype = "controller"

        lang = "js" if js else "ts"

        all_modules = glob(os.path.join(path, "*.module.ts"))
        module_exists = len(all_modules) > 0

        if not module_exists:
            console.warn(
                f"Controller cannot be used without being attached to a module. If you wish to create module '{name}.module.{lang}', use command 'devtools nest module {name}'."
            )
            if not os.path.exists(path):
                os.makedirs(path)

        template = templates.nest_controller(name, lang)

        lib.write_files([template], path)

        if module_exists:
            if len(all_modules) == 1:
                module_name = os.path.basename(all_modules[0])
                lib.modify_module("", name, filetype)
            else:
                console.warn(f"More than one module file has been found in '{path}'. Controller will not be attached to a module.")

        console.log_created(filetype, path, [template["name"]])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")


def service(path: str, js: bool = False, flat: bool = False) -> None:
    try:
        name, path = lib.split_path(path, flat)
        filetype = "service"
        lang = "js" if js else "ts"

        all_modules = glob(os.path.join(path, "*.module.ts"))
        module_exists = len(all_modules) > 0

        if not module_exists:
            console.warn(
                f"{filetype.capitalize()} cannot be used without being attached to a module. If you wish to create module '{name}.module.{lang}', use command 'devtools nest module {name}'."
            )
            if not os.path.exists(path):
                os.makedirs(path)
        template = templates.nest_service(name, lang)

        lib.write_files([template], path)

        if module_exists:
            if len(all_modules) == 1:
                lib.modify_module(all_modules[0], name, filetype)
            else:
                console.warn(f"More than one module file has been found in '{path}'. Service will not be attached to a module.")

        console.log_created(filetype, path, [template["name"]])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")


def entity(
    path: str,
    js: bool = False,
    orm: str = "tyeorm",
    use_uuid: bool = True,
    flat: bool = False
):
    try:
        name, path = lib.split_path(path, flat)

        lang = "js" if js else "ts"

        if not os.path.exists(os.path.join(path)):
            os.makedirs(path)

        template = templates.nest_entity(name, lang, orm, use_uuid)
        lib.write_files([template], path)

        console.log_created("entity", path, [template["name"]])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")


def microservice(path: str, js: bool = False) -> None:
    try:
        _, path = lib.split_path(path)
        src = os.path.join(path, "src")
        lang = "js" if js else "ts"

        console.log("Finding Node.js and npm...")

        node_version = lib.find_node()

        if node_version:
            console.info(f"Node.js v{node_version}")
        else:
            console.error("Node.js not found on this machine.")
            return

        npm, npm_version = lib.find_npm()

        if npm_version:
            console.info(f"npm v{npm_version}")
        else:
            console.error("npm not found on this machine.")
            return

        if not os.path.exists(path):
            os.makedirs(path)

        console.log(lib.SEP)
        console.log("Creating Node.js project...")

        subprocess.run([npm, "init", "-y"], cwd=path, capture_output=True, text=True)
        console.info("Node.js project successfully created!")

        console.log(lib.SEP)
        console.log("Modifying package.json...")

        package_json = lib.read_package_json(at=path)

        package_json["type"] = "module"
        package_json["main"] = f"src/main.{lang}"
        package_json["scripts"]["dev"] = "nodemon --exec tsx src/main.ts"

        lib.rewrite_package_json(at=path, package_json=package_json)

        console.info("package.json successfully modified!")

        console.log(lib.SEP)
        console.log("Installing npm packages...")

        subprocess.run(
            [
                npm,
                "i",
                "@nestjs/core",
                "@nestjs/common",
                "@nestjs/platform-express",
                "@nestjs/microservices",
                "reflect-metadata",
                "rxjs",
                "class-validator",
                "class-transformer",
            ],
            cwd=path,
            capture_output=True,
            text=True,
        )
        if not js:
            subprocess.run(
                [
                    npm,
                    "i",
                    "-D",
                    "@types/node",
                    "typescript",
                    "tsx",
                    "tsconfig-paths",
                    "nodemon"
                ],
                cwd=path,
                capture_output=True,
                text=True,
            )

        console.info("npm packages sucessfully installed!")

        console.log(lib.SEP)
        console.log("Creating template files..")

        if os.path.exists(src):
            console.error(f"Path '{src}' already exists. Aborting to avoid overwriting files.")
            return

        os.mkdir(src)

        console.log(lib.SEP)
        console.log("Creating template files...")

        root_files = [
            {"name": ".gitignore", "content": templates.nest_gitignore()},
            {"name": "tsconfig.json", "content": [templates.nest_tsconfig()]},
            {"name": "Dockerfile", "content": templates.nest_dockerfile()},
        ]

        src_files = [
            templates.nest_main(lang),
            templates.nest_module("app", lang, True, True),
            templates.nest_controller("app", lang),
            templates.nest_service("app", lang),
        ]

        lib.write_files(root_files, path)

        lib.write_files(src_files, src)
        console.info("Template files created!")

        console.log(lib.SEP)
        console.log_created(
            "microservice project", path, [file["name"] for file in src_files]
        )
        print(lib.SEP)
    except KeyboardInterrupt:
        console.error("Operation was aborted.")