import os
from . import templates
from .. import lib
import subprocess
import json


def feature(
    path: str,
    orm: str = "tyeorm",
    use_uuid: bool = True,
    js: bool = False,
    no_entity: bool = True,
    no_controller: bool = False,
    no_service: bool = False,
) -> None:
    try:
        name, path = lib.split_path(path)

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

        lib.log_created("feature", path, [file["name"] for file in files])
    except KeyboardInterrupt:
        lib.error("Operation was aborted.")


def module(path: str, js: bool = False) -> None:
    try:
        name, path = lib.split_path(path)
        file_type = "module"

        if not os.path.exists(path):
            os.makedirs(path)

        lang = "js" if js else "ts"

        template = templates.nest_module(name, lang, controller=False, service=False)
        lib.write_files([template], path)

        lib.log_created(file_type, path, [template["name"]])
    except KeyboardInterrupt:
        lib.error("Operation was aborted.")


def controller(path: str, js: bool = False) -> None:
    try:
        name, path = lib.split_path(path)
        file_type = "controller"

        lang = "js" if js else "ts"

        module_exists = os.path.exists(os.path.join(path, f"{name}.module.{lang}"))

        if not module_exists:
            lib.warn(
                f"Controller cannot be used without being attached to non-existent module '{name}.module.{lang}'. Consider making it before implementing the controller"
            )
            if not os.path.exists(path):
                os.makedirs(path)

        template = templates.nest_controller(name, lang)

        lib.write_files([template], path)

        if module_exists:
            lib.modify_module(os.path.join(path, name, f"{name}.module.{lang}"), file_type)

        lib.log_created(file_type, path, [template["name"]])
    except KeyboardInterrupt:
        lib.error("Operation was aborted.")


def service(path: str, js: bool = False) -> None:
    try:
        name, path = lib.split_path(path)
        file_type = "service"
        lang = "js" if js else "ts"

        module_exists = os.path.exists(os.path.join(path, f"{name}.module.{lang}"))

        if not module_exists:
            lib.warn(
                f"Service cannot be used without being attached to non-existent module '{name}.module.{lang}'. Consider making it before implementing the service."
            )
            if not os.path.exists(path):
                os.makedirs(path)
        template = templates.nest_service(name, lang)

        lib.write_files([template], path)

        if module_exists:
            lib.modify_module(os.path.join(path, name, f"{name}.module.{lang}"), file_type)

        lib.log_created(file_type, path, [template["name"]])
    except KeyboardInterrupt:
        lib.error("Operation was aborted.")


def entity(
    path: str,
    js: bool = False,
    orm: str = "tyeorm",
    use_uuid: bool = True,
):
    try:
        name, path = lib.split_path(path)

        lang = "js" if js else "ts"

        if not os.path.exists(os.path.join(path)):
            os.makedirs(path)

        template = templates.nest_entity(name, lang, orm, use_uuid)
        lib.write_files([template], path)

        lib.log_created("entity", path, [template["name"]])
    except KeyboardInterrupt:
        lib.error("Operation was aborted.")


def microservice(path: str, js: bool = False) -> None:
    try:
        _, path = lib.split_path(path)
        src = os.path.join(path, "src")
        lang = "js" if js else "ts"

        node_version = lib.find_node()

        if node_version:
            print(f"Node.js v{node_version}")
        else:
            lib.error("Node.js not found on this machine.")
            return

        npm, npm_version = lib.find_npm()

        if npm_version:
            print(f"npm v{npm_version}")
        else:
            lib.error("npm not found on this machine.")
            return

        if not os.path.exists(path):
            os.makedirs(path)

        print(lib.SEP)
        print("Creating Node.js project...")

        subprocess.run([npm, "init", "-y"], cwd=path, capture_output=True, text=True)

        print(lib.SEP)
        print("Modifying package.json...")

        package_json = lib.read_package_json(at=path)

        package_json["type"] = "module"
        package_json["main"] = f"src/main.{lang}"

        lib.rewrite_package_json(at=path, package_json=package_json)

        print("package.json successfully modified.")

        print(lib.SEP)
        print("Installing npm packages...")

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
                    "ts-node",
                    "tsconfig-paths",
                ],
                cwd=path,
                capture_output=True,
                text=True,
            )

        print("npm packages installed.")

        print(lib.SEP)
        print("Creating template files..")

        if os.path.exists(src):
            print(
                f"Error: '{src}' already exists. Aborting to avoid overwriting files."
            )
            return

        os.mkdir(src)

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
        print("Template files created.")

        print(lib.SEP)
        lib.log_created(
            "microservice project", path, [file["name"] for file in src_files]
        )
        print(lib.SEP)
    except KeyboardInterrupt:
        lib.error("Operation was aborted.")
