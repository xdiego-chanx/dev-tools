from src.config.ConfigRules import ConfigRules
from src.util.ImportMeta import ImportMeta
from src.util.NameManager import NameManager
from src.util.TemplateBase import TemplateBase


class NestTemplates:
    meta: ImportMeta
    nm: NameManager
    rules: ConfigRules

    def __init__(self):
        self.meta = ImportMeta.instance()
        self.nm = NameManager()
        self.rules = ConfigRules()

    def module(
        self: type["NestTemplates"],
        name: str,
        lang: str,
        controller: bool,
        provider: bool,
    ) -> TemplateBase:
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.module.{lang}"

        imports = [
            f"import {{{self.rules.obj_space}Module{self.rules.obj_space}}} from {self.rules.quote}@nestjs/common{self.rules.quote}{self.rules.semicolon}"]

        if controller:
            imports.append(f"import {{{self.rules.obj_space}{pascal_name}Controller{self.rules.obj_space}}} from {self.rules.quote}./{name}.controller{self.rules.quote}{self.rules.semicolon}")
        if provider:
            imports.append(f"import {{{self.rules.obj_space}{pascal_name}Service{self.rules.obj_space}}} from {self.rules.quote}./{name}.service{self.rules.quote}{self.rules.semicolon}")
        
        contents = [
            *imports,
            "",
            "@Module({",
            f"{self.rules.indent}controllers: [{f"{pascal_name}Controller" if controller else ""}],"
            f"{self.rules.indent}providers: [{f"{pascal_name}Service" if provider else ""}]{self.rules.trailing_comma}",
            "})",
            f"export class {pascal_name}Module{self.rules.bracket_space}{{{self.rules.bracket_space or " "}}}"
        ]

        return TemplateBase(filename, contents)
    
    def controller(
        self: type["NestTemplates"],
        name: str,
        lang: str,
    ) -> TemplateBase:
        camel_name = self.nm.switch(name, self.nm.kebab, self.nm.camel)
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.controller.{lang}"

        contents = [
            f"import {{{self.rules.obj_space}Controller{self.rules.obj_space}}} from {self.rules.quote}@nestjs/common{self.rules.quote};",
            "",
            f"@Controller({self.rules.quote}{name}{self.rules.quote})",
            f"export class {pascal_name}Controller{self.rules.bracket_space}{{",
            f"{self.rules.indent}constructor(private readonly {camel_name}Service: {pascal_name}Service){self.rules.bracket_space}{{{self.rules.bracket_space or " "}}}",
            "}"
        ]

        return TemplateBase(filename, contents)
    
    def service( 
        self: type["NestTemplates"],
        name: str,
        lang: str,
    ) -> TemplateBase:
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.service.{lang}"
        contents = [
            f"import {{{self.rules.obj_space}Injectable{self.rules.obj_space}}} from {self.rules.quote}@nestjs/common{self.rules.quote}{self.rules.semicolon}",
            "",
            f"@Injectable()",
            f"export class {pascal_name}Controller{self.rules.bracket_space}{{",
            f"{self.rules.indent}",
            "}"
        ]

        return TemplateBase(filename, contents)
    
    def typeorm_entity(        
        self: type["NestTemplates"],
        name: str,
        lang: str,
    ) -> TemplateBase:
        snake_name = self.nm.switch(name, self.nm.kebab, self.nm.snake)
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.entity.{lang}"

        contents = [
            f"import {{{self.rules.obj_space}Entity, PrimaryGeneratedColumn{self.rules.obj_space}}} from {self.rules.quote}typeorm{self.rules.quote}{self.rules.semicolon}",
            "",
            f"@Entity({self.rules.quote}{snake_name}{self.rules.quote})",
            f"export class {pascal_name} {{",
            f"@PrimaryGeneratedColumn({self.rules.quote}uuid{self.rules.quote})",
            f"id!: string{self.rules.semicolon}",
            "}"
        ]

        return TemplateBase(filename, contents)




# import { Entity, PrimaryGeneratedColumn } from "typeorm";

# @Entity()
# export class ExampleEntity {
#   @PrimaryGeneratedColumn("uuid")
#   id: string;
# }

    
