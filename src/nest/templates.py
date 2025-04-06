from .. import lib
import json


def nest_module(
    name: str, lang: str, controller: bool, service: bool
) -> dict[str, str | list[str]]:
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)
    imports = ['import { Module } from "@nestjs/common";']

    if controller:
        imports.append(
            f'import {{ {pascal_name}Controller }} from "./{name}.controller";'
        )
    if service:
        imports.append(f'import {{ {pascal_name}Service }} from "./{name}.service";')
    if controller or service:
        imports.append("")

    module = {
        "name": f"{name}.module.{lang}",
        "content": [
            "@Module({",
            lib.TAB + "imports: [],",
            f"{lib.TAB}controllers: [{f"{pascal_name}Controller" if controller else ""}],",
            f"{lib.TAB}providers: [{f"{pascal_name}Service" if service else ""}],",
            "})",
            f"export class {pascal_name}Module {{ }}",
        ],
    }

    module["content"] = imports + module["content"]
    return module


def nest_controller(name: str, lang: str) -> dict[str, str | list[str]]:
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)
    camel_name = lib.switch_naming_conv(name, lib.kebab, lib.camel)
    js_content = [
        'import { Controller } from "@nestjs/common";',
        f'import {{ {pascal_name}Service }} from "./{name}.service";',
        "",
        f'@Controller("{name}")',
        f"export class {pascal_name}Controller {{",
        f"{lib.TAB}constructor({camel_name}Service) {{ }}",
        "}",
    ]
    ts_content = [
        'import { Controller } from "@nestjs/common";',
        f'import {{ {pascal_name}Service }} from "./{name}.service";',
        "",
        f'@Controller("{name}")',
        f"export class {pascal_name}Controller {{",
        f"{lib.TAB}constructor(private readonly {camel_name}Service: {pascal_name}Service) {{ }}",
        "}",
    ]

    return {
        "name": f"{name}.controller.{lang}",
        "content": js_content if lang == "js" else ts_content,
    }


def nest_service(name: str, lang: str) -> dict[str, str | list[str]]:
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)
    return {
        "name": f"{name}.service.{lang}",
        "content": [
            'import { Injectable } from "@nestjs/common";',
            "",
            "@Injectable()",
            f"export class {pascal_name}Service {{",
            lib.TAB,
            "}",
        ],
    }


def nest_entity(
    name: str, lang: str, orm: str = "typeorm", use_uuid: bool = True
) -> dict[str, str | list[str]]:
    filename = f"{name}.entity.{lang}"
    snake_name = lib.switch_naming_conv(name, lib.kebab, lib.snake)
    pascal_name = lib.switch_naming_conv(name, lib.kebab, lib.pascal)

    js_pk_typeorm = lib.TAB + "id;"
    ts_pk_typeorm = f"{lib.TAB}id: {"string" if use_uuid else "number"};"
    orm_typeorm = [
        'import { Entity, PrimaryGeneratedColumn } from "typeorm";',
        "",
        f'@Entity("{snake_name}")',
        f"export class {pascal_name} {{",
        f"{lib.TAB}@PrimaryGeneratedColumn({"\"uuid\"" if use_uuid else ""})",
        js_pk_typeorm if lang == "js" else ts_pk_typeorm,
        "}",
    ]

    orm_sequelize = [
        f'import {{ Column, Model, Table, DataType{", Default" if use_uuid else ""} }} from "sequelize-typescript";',
        "",
        "@Table",
        f"export class {pascal_name} extends Model {{",
        lib.TAB + "@PrimaryKey",
        f"{lib.TAB}{"@Default(DataType.UUIDV4)" if use_uuid else "@AutoIncrement"}",
        f"{lib.TAB}@Column({"{type: DataType.UUID}" if use_uuid else ""})",
        js_pk_typeorm if lang == "js" else ts_pk_typeorm,
        "}",
    ]

    if orm == "typeorm":
        return {"name": filename, "content": orm_typeorm}
    elif orm == "sequelize":
        return {"name": filename, "content": orm_sequelize}
    pass


def nest_main(lang: str) -> dict[str, str | list[str]]:
    return {
        "name": f"main.{lang}",
        "content": [
            'import { NestFactory } from "@nestjs/core";',
            'import { AppModule } from "./app.module";',
            "",
            "(async () => {",
            f"{lib.TAB}const app = await NestFactory.create(AppModule);",
            lib.TAB,
            f'{lib.TAB}const host = process.env.HOST ?? "127.0.0.1";',
            f"{lib.TAB}const port = process.env.PORT ?? 3000;",
            lib.TAB,
            f'{lib.TAB}await app.listen(port, () => console.log("Server is listening at http://%s:%d/", host, port));',
            "})();",
        ],
    }


def nest_dockerfile() -> list[str]:
    return [
        "# auto-generated Dockerfile",
        "FROM node:22-alpine AS build",
        "",
        "WORKDIR /build",
        "",
        "COPY package.json package-lock.json* /build/",
        "RUN npm install",
        "",
        "COPY ./src /build",
        "",
        "RUN npm run build",
        "",
        "FROM node:22-alpine AS prod",
        "",
        "WORKDIR /app",
        "",
        "COPY --from=build /build/dist /app/dist",
        "ENV NODE_ENV=production",
        'CMD ["node", "/app/dist/index.js"]',
    ]


def nest_tsconfig() -> str:
    return json.dumps(
        {
            "compilerOptions": {
                "target": "ES2020",
                "module": "ES6",
                "moduleResolution": "node",
                "experimentalDecorators": True,
                "emitDecoratorMetadata": True,
                "allowJs": True,
                "checkJs": False,
                "strict": True,
                "skipLibCheck": True,
                "esModuleInterop": True,
                "forceConsistentCasingInFileNames": True,
                "outDir": "./dist",
                "baseUrl": "./",
                "paths": {"@/*": ["src/*"]},
            },
            "include": ["src/**/*.ts"],
            "exclude": ["node_modules", "dist"],
        },
        indent=4,
    )


def nest_gitignore() -> list[str]:
    return [
        "packages/*/package-lock.json",
        "sample/**/package-lock.json",
        "",
        "# dependencies",
        "node_modules/",
        "",
        "# Distribution files",
        "dist/",
        "",
        "# IDE",
        "/.idea",
        "/.awcache",
        "/.vscode",
        "/.devcontainer",
        "/.classpath",
        "/.project",
        "/.settings",
        "*.code-workspace",
        "",
        "# Vim",
        "[._]*.s[a-v][a-z]",
        "[._]*.sw[a-p]",
        "[._]s[a-rt-v][a-z]",
        "[._]ss[a-gi-z]",
        "[._]sw[a-p]",
        "# bundle",
        "packages/**/*.d.ts",
        "packages/**/*.js",
        "",
        "# misc",
        ".DS_Store",
        "lerna-debug.log",
        "npm-debug.log",
        "yarn-error.log",
        "/**/npm-debug.log",
        "/packages/**/.npmignore",
        "/packages/**/LICENSE",
        "*.tsbuildinfo",
        "",
        "# example",
        "/quick-start",
        "/example_dist",
        "/example",
        "",
        "# tests",
        "/test",
        "/benchmarks/memory",
        "/coverage",
        "/.nyc_output",
        "/packages/graphql",
        "/benchmarks/memory",
        "build/config.gypi",
        "",
        ".npmrc",
        "pnpm-lock.yaml",
        "/.history",
    ]
