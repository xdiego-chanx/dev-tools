from . import lib

def react_module(name, lang):
    return {
        f"{name}.{lang}": [
            f"import styles from \"./{name}.module.css\";",
            "",
            f"export default function {name}() {"{"}",
            lib.space(4) + "return(",
            lib.space(8) + "<>",
            lib.space(12) + "",
            lib.space(8) + "</>",
            lib.space(4) + ");",
            "}"                                   
        ],
        f"{name}.module.css": [
            f"/* {name} CSS Module */"
        ]
    }

def aspnet_module(namespace, name):
    return {
        f"{name}Controller": [
            "using Microsoft.AspNetCore.Mvc;",
            "",
            f"namespace {namespace};",
            "",
            "[ApiController]",
            "[Route(\"api/[controller]\")]",
            f"public class {name}Controller : ControllerBase",
            "{",
            lib.space(4),
            "}",
        ],
        f"I{name}Service": [
            f"namespace {namespace};",
            "",
            f"public interface I{name}Service",
            "{",
            lib.space(4),
            "}",
        ],
        f"{name}Provider": [
            f"namespace {namespace};",
            "",
            f"public class {name}Provider",
            "{",
            lib.space(4),
            "}",
        ],
        f"{name}Entity": [
            f"namespace {namespace};",
            "",
            f"public class {name}Entity",
            "{",
            lib.space(4),
            "}",
        ],
        f"{name}Repository": [
            f"namespace {namespace};",
            "",
            f"public class {name}Repository",
            "{",
            lib.space(4),
            "}",
        ]
    }

def nestjs_module(name, lang):
    return {
        f"{name}.controller.{lang}": [
            "import { Controller } from \"@nestjs/common\";",
            f"import {"{ " + lib.capitalize_name(name) + "Service }"} from \"./{name}.service\";",
            "",
            "@Controller()",
            f"export class {lib.capitalize_name(name)}Controller {"{"}",
            f"{lib.space(4)}private readonly {name}Service: {lib.capitalize_name(name)}Service;",
            lib.space(4),
            f"{lib.space(4)}constructor({name}Service: {lib.capitalize_name(name)}Service) {"{"}",
            f"{lib.space(8)}this.{name}Service = {name}Service;",
            f"{lib.space(4)}{"}"}",
            "}"
        ],
        f"{name}.module.{lang}": [
            "import { Module } from \"@nestjs/common\";",
            "import { TypeOrmModule } from \"@nestjs/typeorm\";",
            f"import {"{ " + lib.capitalize_name(name) + "Controller }"} from \"./{name}.controller\";",
            f"import {"{ " + lib.capitalize_name(name) + "Service }"} from \"./{name}.service\";",
            f"import {"{ " + lib.capitalize_name(lib.singularize_name(name)) + " }"} from \"./{name}.entity\";",
            "",
            "@Module({",
            f"{lib.space(4)}imports: [TypeOrmModule.forFeature([{lib.capitalize_name(lib.singularize_name(name))}])],",
            f"{lib.space(4)}controllers: [{lib.capitalize_name(name)}Controller],",
            f"{lib.space(4)}providers: [{lib.capitalize_name(name)}Service]",
            "})",
            f"export class {lib.capitalize_name(name)}Module {"{}"}",
        ],
        f"{name}.service.{lang}": [
            "import { Injectable } from \"@nestjs/common\";",
            "",
            "@Injectable()",
            f"export class {lib.capitalize_name(name)}Service {"{"}",
            lib.space(4),
            "}"
        ],
        f"{name}.entity.{lang}": [
            "import { Entity } from \"typeorm\";",
            "",
            "@Entity()",
            f"export class {lib.capitalize_name(lib.singularize_name(name)) + " {"}",
            lib.space(4),
            "}"
        ]
    }