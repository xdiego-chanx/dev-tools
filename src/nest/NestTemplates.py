from typing import Any
from src.config.ConfigRules import ConfigRules
from src.config.ConfigProfile import ConfigProfile
from src.util.ImportMeta import ImportMeta
from src.util.TemplateBase import TemplateBase


class NestTemplates:
    meta: ImportMeta
    config: ConfigProfile
    rules: ConfigRules

    def __init__(self):
        self.meta = ImportMeta.instance()
        self.rules = ConfigRules()

    def module(
        self: type["NestTemplates"],
        name: str,
        lang: str,
        controller: bool,
        provider: bool,
    ) -> TemplateBase:
        filename = f"{name}.module.{lang}"

        imports = ["import { Module } from \"@nestjs/common\";"]

        if controller:
            imports.append(f"import {{ {name}Controller }} from \"./{name}.controller\"; ")
        if provider:
            imports.append(f"import {{ {name}Service }} from \"./{name}.service\"; ")
        
        contents = [
            *imports,
            "",
            "@Module({",
            f"{self.rules.indent}controllers: [{f"{name}Controller" if controller else ""}],"
            f"{self.rules.indent}providers: [{f"{name}Service" if provider else ""}]{self.rules.trailing_comma}",
            "})",
            f"export class {name}Module {{ }}"
        ]

        return TemplateBase(filename, contents)
    