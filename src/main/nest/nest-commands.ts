import { interruptible, requires } from "@lib/decorators";
import { CommandBase } from "@main/lib/command-base";
import { NestTemplates } from "./nest-templates";
import { Template } from "@main/lib/template";

export class NestCommands extends CommandBase {

    @interruptible()
    @requires("path")
    @requires("flat")
    public createResource(args: Map<ArgK, ArgV>): void {
        const flat = args.get("flat") as boolean;
        console.log("flat: %o", flat);
        const [name, filepath] = this.splitPath(args.get("path") as string, flat);
        const templates: Array<Template> = [
            NestTemplates.module(name),
            NestTemplates.controller(name),
            NestTemplates.service(name)
        ];

        this.buildFiles(templates, { at: filepath });

        this.logDirectoryStructure(filepath, {
            filename: name,
            filetype: "resource",
            createdFiles: templates.map((template) => template.filename)
        });
    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createModule(args: Map<ArgK, ArgV>): void {
        const flat = args.get("flat") as boolean;
        const [name, filepath] = this.splitPath(args.get("path") as string, flat);
        const templates: Array<Template> = [
            NestTemplates.module(name)
        ];

        this.buildFiles(templates, { at: filepath });

        this.logDirectoryStructure(filepath, {
            filename: name,
            filetype: "module",
            createdFiles: templates.map((template) => template.filename)
        });
    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createController(args: Map<ArgK, ArgV>): void {
        const flat = args.get("flat") as boolean;
        const [name, filepath] = this.splitPath(args.get("path") as string, flat);
        const templates: Array<Template> = [
            NestTemplates.controller(name)
        ];

        this.buildFiles(templates, { at: filepath });

        this.logDirectoryStructure(filepath, {
            filename: name,
            filetype: "controller",
            createdFiles: templates.map((template) => template.filename)
        });
    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createService(args: Map<ArgK, ArgV>): void {
        const flat = args.get("flat") as boolean;
        const [name, filepath] = this.splitPath(args.get("path") as string, flat);
        const templates: Array<Template> = [
            NestTemplates.service(name)
        ];

        this.buildFiles(templates, { at: filepath });

        this.logDirectoryStructure(filepath, {
            filename: name,
            filetype: "service",
            createdFiles: templates.map((template) => template.filename)
        });
    }

    @interruptible()
    @requires("path")
    @requires("flat")
    @requires("orm")
    public createEntity(args: Map<ArgK, ArgV>): void {
        const flat = args.get("flat") as boolean;
        const [name, filepath] = this.splitPath(args.get("path") as string, flat);
    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createProject(args: Map<ArgK, ArgV>): void {
        const flat = args.get("flat") as boolean;
        const [name, filepath] = this.splitPath(args.get("path") as string, flat);
    }

    @interruptible()
    @requires("path")
    @requires("flat")
    public createMicroservice(args: Map<ArgK, ArgV>): void {
        const flat = args.get("flat") as boolean;
        const [name, filepath] = this.splitPath(args.get("path") as string, flat);
    }
}