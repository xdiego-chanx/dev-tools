from src.util.ImportMeta import ImportMeta
from src.util.NameManager import NameManager
from src.util.TemplateBase import TemplateBase


class NestTemplates:
    meta: ImportMeta
    nm: NameManager

    def __init__(self):
        self.meta = ImportMeta.instance()
        self.nm = NameManager()

    def module(
        self,
        name: str,
        controller: bool,
        provider: bool,
    ) -> TemplateBase:
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.module.ts"

        imports = [
            f"import {{ Module }} from \"@nestjs/common\";"
        ]

        if controller:
            imports.append(
                f"import {{ {pascal_name}Controller }} from \"./{name}.controller\";"
            )
        if provider:
            imports.append(
                f"import {{ {pascal_name}Service }} from \"./{name}.service\";"
            )

        contents = [
            *imports,
            "",
            "@Module({",
            f"{" " * 4}imports: [],"
            f"{" " * 4}controllers: [{f"{pascal_name}Controller" if controller else ""}],",
            f"{" " * 4}providers: [{f"{pascal_name}Service" if provider else ""}]",
            "})",
            f"export class {pascal_name}Module {{ }}",
        ]

        return TemplateBase(filename, "create", contents)

    def controller(
        self,
        name: str,
    ) -> TemplateBase:
        camel_name = self.nm.switch(name, self.nm.kebab, self.nm.camel)
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.controller.ts"

        contents = [
            f"import {{ Controller }} from \"@nestjs/common\";",
            f"import {{ {pascal_name}Service }} from \"./{name}.service\";"
            "",
            f"@Controller(\"{name}\")",
            f"export class {pascal_name}Controller {{",
            f"{" " * 4}constructor(private readonly {camel_name}Service: {pascal_name}Service) {{ }}",
            "}",
        ]

        return TemplateBase(filename, "create", contents)

    def service(
        self,
        name: str,
    ) -> TemplateBase:
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.service.ts"
        contents = [
            f"import {{ Injectable }} from \"@nestjs/common\";",
            "",
            f"@Injectable()",
            f"export class {pascal_name}Service {{",
            f"{" " * 4}",
            "}",
        ]

        return TemplateBase(filename, "create", contents)

    def typeorm_entity(
        self,
        name: str,
    ) -> TemplateBase:
        snake_name = self.nm.switch(name, self.nm.kebab, self.nm.snake)
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.entity.ts"

        contents = [
            f"import {{ Entity, PrimaryGeneratedColumn }} from \"typeorm\";",
            "",
            f"@Entity(\"{snake_name}\")",
            f"export class {pascal_name} {{",
            f"{" " * 4}@PrimaryGeneratedColumn(\"uuid\")",
            f"{" " * 4}id!: string;",
            "}",
        ]

        return TemplateBase(filename, "create", contents)

    def prisma_entity(
        self,
        name: str
    ) -> TemplateBase:
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = "schema.prisma"

        contents = [
            f"model {pascal_name} {{",
            f"{" " * 4}id String @id @default(uuid())",
            "}"
        ]

        return TemplateBase(filename, "update", contents)
    
    def sequelize_entity(
        self,
        name: str,
    ) -> TemplateBase:
        pascal_name = self.nm.switch(name, self.nm.kebab, self.nm.pascal)
        filename = f"{name}.entity.ts"

        contents = [
            f"import {{ Table, Column, Model }} from \"sequelize-typescript\";",
            "",
            "@Table",
            f"export class {pascal_name} extends Model {{",
            "@Column",
            f"name: string;",
            "}"
        ]

        return TemplateBase(filename, "create", contents)

