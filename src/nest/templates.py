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
    ts_pk_typeorm = f"{lib.TAB}id!: {"string" if use_uuid else "number"};"
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


def nest_bun_dockerfile() -> list[str]:
    return [
        "# auto-generated Dockerfile",
        "FROM oven/bun:1 AS prod",
        "",
        "WORKDIR /app",
        "",
        "COPY bun.lock /app/",
        "COPY package.json /app/",
        "RUN bun install --frozen-lockfile",
        "",
        "COPY . /app",
        "",
        "ENV NODE_ENV=production",
        'CMD ["bun", "src/index.ts"]'
    ]


def nest_node_dockerfile() -> list[str]:
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
                "target": "ESNext",
                "module": "ESNext",
                "moduleDetection": "force",
                "moduleResolution": "bundler",
                "allowImportingTsExtensions": True,
                "verbatimModuleSyntax": True,
                "noEmit": True,
                "experimentalDecorators": True,
                "emitDecoratorMetadata": True,
                "baseUrl": "./",
                "paths": {"@/*": ["src/*"]},
                "strict": True,
                "skipLibCheck": True,
                "noFallthroughCasesInSwitch": True,
                "strictNullChecks": True,
                "forceConsistentCasingInFileNames": True,
                "allowSyntheticDefaultImports": True,
                "noImplicitAny": False,
                "noUnusedLocals": False,
                "noUnusedParameters": False,
                "noPropertyAccessFromIndexSignature": False,
            },
            "include": ["src/**/*.ts"],
            "exclude": ["node_modules", "dist"],
        },
        indent=4,
    )


def nest_gitignore() -> list[str]:
    return [
        "# Logs",
        "logs",
        "*.log",
        "npm-debug.log*",
        "yarn-debug.log*",
        "yarn-error.log*",
        "lerna-debug.log*",
        ".pnpm-debug.log*",
        "",
        "# Diagnostic reports (https://nodejs.org/api/report.html)",
        "report.[0-9]*.[0-9]*.[0-9]*.[0-9]*.json",
        "",
        "# Runtime data",
        "pids",
        "*.pid",
        "*.seed",
        "*.pid.lock",
        "",
        "# Directory for instrumented libs generated by jscoverage/JSCover",
        "lib-cov",
        "",
        "# Coverage directory used by tools like istanbul",
        "coverage",
        "*.lcov",
        "",
        "# nyc test coverage",
        ".nyc_output",
        "",
        "# Grunt intermediate storage (https://gruntjs.com/creating-plugins#storing-task-files)",
        ".grunt",
        "",
        "# Bower dependency directory (https://bower.io/)",
        "bower_components",
        "",
        "# node-waf configuration",
        ".lock-wscript",
        "",
        "# Compiled binary addons (https://nodejs.org/api/addons.html)",
        "build/Release",
        "",
        "# Dependency directories",
        "node_modules/",
        "jspm_packages/",
        "",
        "# Snowpack dependency directory (https://snowpack.dev/)",
        "web_modules/",
        "",
        "# TypeScript cache",
        "*.tsbuildinfo",
        "",
        "# Optional npm cache directory",
        ".npm",
        "",
        "# Optional eslint cache",
        ".eslintcache",
        "",
        "# Optional stylelint cache",
        ".stylelintcache",
        "",
        "# Microbundle cache",
        ".rpt2_cache/",
        ".rts2_cache_cjs/",
        ".rts2_cache_es/",
        ".rts2_cache_umd/",
        "",
        "# Optional REPL history",
        ".node_repl_history",
        "",
        "# Output of 'npm pack'",
        "*.tgz",
        "",
        "# Yarn Integrity file",
        ".yarn-integrity",
        "",
        "# dotenv environment variable files",
        ".env",
        ".env.development.local",
        ".env.test.local",
        ".env.production.local",
        ".env.local",
        "",
        "# parcel-bundler cache (https://parceljs.org/)",
        ".cache",
        ".parcel-cache",
        "",
        "# Next.js build output",
        ".next",
        "out",
        "",
        "# Nuxt.js build / generate output",
        ".nuxt",
        "dist",
        "",
        "# Gatsby files",
        ".cache/",
        "# Comment in the public line in if your project uses Gatsby and not Next.js",
        "# https://nextjs.org/blog/next-9-1#public-directory-support",
        "# public",
        "",
        "# vuepress build output",
        ".vuepress/dist",
        "",
        "# vuepress v2.x temp and cache directory",
        ".temp",
        ".cache",
        "",
        "# vitepress build output",
        "**/.vitepress/dist",
        "",
        "# vitepress cache directory",
        "**/.vitepress/cache",
        "",
        "# Docusaurus cache and generated files",
        ".docusaurus",
        "",
        "# Serverless directories",
        ".serverless/",
        "",
        "# FuseBox cache",
        ".fusebox/",
        "",
        "# DynamoDB Local files",
        ".dynamodb/",
        "",
        "# TernJS port file",
        ".tern-port",
        "",
        "# Stores VSCode versions used for testing VSCode extensions",
        ".vscode-test",
        "",
        "# yarn v2",
        ".yarn/cache",
        ".yarn/unplugged",
        ".yarn/build-state.yml",
        ".yarn/install-state.gz",
        ".pnp.*",
    ]
