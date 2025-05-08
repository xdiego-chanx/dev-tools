import { Case } from "@main/lib/case";
import { CasingManager } from "@main/lib/casing-manager";
import { Template } from "@main/lib/template";
import { TAB } from "@main/lib/utils";

export class NestTemplates {
    private static casing: CasingManager = CasingManager.instance;

    public static module(name: string): Template {
        const pascal: string = this.casing.change(name, Case.Kebab, Case.Pascal);
        return {
            filename: `${name}.module.ts`,
            contents: [
                "import { Module } from \"@nestjs/common\";",
                `import {${pascal}Controller} from "./${name}.controller";`,
                `import {${pascal}Service} from "./${name}.service";`,
                "",
                "@Module({",
                TAB + "imports: [],",
                TAB + `controllers: [${pascal}Controller],`,
                TAB + `providers: [${pascal}Service],`,
                TAB + "exports: []",
                "})",
                `export class ${pascal}Module { }`
            ]
        };
    }

    public static controller(filename: string): Template {
        const camel: string = this.casing.change(filename, Case.Kebab, Case.Camel);
        const pascal: string = this.casing.change(filename, Case.Kebab, Case.Pascal);
        return {
            filename: `${filename}.controller.ts`,
            contents: [
                "import { Controller } from \"@nestjs/common\";",
                `import {${pascal}Service} from "./${filename}.service;"`,
                "",
                `@Controller("${filename}")`,
                `export class ${pascal}Controller {`,
                TAB + `constructor(private readonly ${camel}Service: ${pascal}Service) {}`,
                "}"
            ]
        };
    }

    public static service(filename: string): Template {
        const pascal: string = this.casing.change(filename, Case.Kebab, Case.Pascal);
        return {
            filename: `${filename}.service.ts`,
            contents: [
                "import { Injectable } from \"@nestjs/common\";",
                "",
                "@Injectable()",
                `export class ${pascal}Service {`,
                TAB,
                "}"
            ]
        };
    }
}