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
    flat: bool = False,
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
                console.warn(
                    f"More than one module file has been found in '{path}'. Controller will not be attached to a module."
                )

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
                console.warn(
                    f"More than one module file has been found in '{path}'. Service will not be attached to a module."
                )

        console.log_created(filetype, path, [template["name"]])
    except KeyboardInterrupt:
        console.error("Operation was aborted.")


def entity(
    path: str,
    js: bool = False,
    orm: str = "tyeorm",
    use_uuid: bool = True,
    flat: bool = False,
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


def microservice(path: str, pm: str, js: bool) -> None:
    try:
        _, path = lib.split_path(path)
        src = os.path.join(path, "src")
        lang = "js" if js else "ts"
        common_pkg = [
            "@nestjs/core",
            "@nestjs/common",
            "@nestjs/platform-express",
            "@nestjs/microservices",
            "reflect-metadata" "rxjs",
            "class-validator",
            "class-transformer",
        ]
        common_dev_pkg = ["@types/node", "jest", "@nestjs/testing", "ts-jest", "@types/jest"]
        npm_dev_pkg = ["typescript", "tsx", "tsconfig-paths", "nodemon"]

        runtime_info = {
            "name": None,
            "package_manager": None,
            "package_install": None,
            "dev_install": None,
            "packages": [],
            "dev_packages": [],
            "dev_script": None,
            "dockerfile": None
        }

        if pm == "npm":
            console.log("Finding Node.js and npm...")
            node_version = lib.find_node()

            if node_version:
                console.info(f"Node.js v{node_version}")
            else:
                console.error("Node.js not found on this machine.")

            npm, npm_version = lib.find_npm()
            if npm_version:
                console.info(f"npm v{npm_version}")
            else:
                console.error("npm not found on this machine.")
                return
            runtime_info["name"] = "Node.js"
            runtime_info["package_manager"] = npm
            runtime_info["package_install"] = "i"
            runtime_info["dev_install"] = "-D"
            runtime_info["packages"] = common_pkg
            runtime_info["dev_packages"] = common_dev_pkg + npm_dev_pkg
            runtime_info["dev_script"] = "nodemon --exec tsx src/main.ts"
            runtime_info["dockerfile"] = templates.nest_npm_dockerfile()

        elif pm == "bun":
            console.log("Finding Bun...")
            bun_version = lib.find_bun()
            if bun_version:
                console.info(f"Bun v{bun_version}")
            else:
                console.error("Bun not found on this machine.")
                return
            runtime_info["name"] = "Bun"
            runtime_info["package_manager"] = "bun"
            runtime_info["package_install"] = "add"
            runtime_info["dev_install"] = "-d"
            runtime_info["packages"] = common_pkg
            runtime_info["dev_packages"] = common_dev_pkg
            runtime_info["dev_script"] = "bun --watch src/main.ts"
            runtime_info["dockerfile"] = templates.nest_bun_dockerfile()

        if not os.path.exists(path):
            os.makedirs(path)

        console.log(lib.SEP)
        console.log(f"Creating {runtime_info["name"]} project...")
        try:
            subprocess.run(
                [runtime_info["package_manager"], "init", "-y"],
                cwd=path,
                capture_output=True,
            )
        except:
            console.error(f"{runtime_info["name"]} project creation was aborted due to an error.")
            return
        else:
            console.log(lib.SEP)
            console.log("Modifying package.json...")
            try:
                package_json = lib.read_package_json(at=path)

                package_json["type"] = "module"
                try:
                    del package_json["main"]
                except KeyError:
                    pass
                package_json["module"] = f"src/main.{lang}"
                package_json["scripts"] = {}
                package_json["scripts"]["test"] = "jest"
                package_json["scripts"]["dev"] = runtime_info["dev_script"]
                lib.rewrite_package_json(at=path, package_json=package_json)
                
                console.info("package.json successfully modified!")

            except:
                console.error("package.json modification was aborted due to an error.")
                return
            else: 
                try: 
                    console.log(lib.SEP)
                    console.log(f"Installing {runtime_info["package_manager"].rstrip(".cmd")} packages...")

                    subprocess.run(
                        ([runtime_info["package_manager"], runtime_info["package_install"]] + runtime_info["packages"]),
                        cwd=path,
                        capture_output=True
                    )

                    subprocess.run(
                        ([runtime_info["package_manager"], runtime_info["package_install"], runtime_info["dev_install"]] + runtime_info["dev_packages"]),
                        cwd=path,
                        capture_output=True
                    )

                    console.info(f"{runtime_info["package_manager"].rstrip(".cmd")} packages sucessfully installed!")
                except:
                    console.error("Package installation was aborted due to an error.")
                    return
                else: 
                    try:
                        console.log(lib.SEP)
                        console.log("Creating template files..")

                        if os.path.exists(src) and os.path.isdir(src):
                            console.error(f"Path '{src}' already exists. Aborting to avoid overwriting files.")
                            return

                        os.mkdir(src)

                        root_files = [
                            {"name": ".gitignore", "content": templates.nest_gitignore()},
                            {"name": "tsconfig.json", "content": [templates.nest_tsconfig()]},
                            {"name": "Dockerfile", "content": runtime_info["dockerfile"]},
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
                    except:
                        console.error("File creation was aborted due to an error.")
                        return
                    else: 
                        console.log(lib.SEP)
                        console.log("Applying cleanup logic...")

                        try:
                            autogenerated_entry_points = [f"main.{lang}", f"index.{lang}", f"app.{lang}", f"server.{lang}"]
                            dir_files = [entry.name for entry in os.scandir(path) if entry.is_file()]

                            for entry_point in autogenerated_entry_points:
                                if entry_point in dir_files:
                                    os.remove(os.path.join(path, entry_point))
                            console.info("Cleanup successful!")
                        except:
                            console.error("Cleanup was aborted due to an error.")
                        else:
                            console.log(lib.SEP)
                            console.log_created( "microservice project", path, [file["name"] for file in src_files])

    except KeyboardInterrupt:
        console.error("Operation was aborted.")