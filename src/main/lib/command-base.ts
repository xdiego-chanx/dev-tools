import path from "path";
import fs from "fs";
import { File } from "./file";
import { Template } from "./template";
import { Logger } from "./logger";
import { TAB } from "./utils";

export abstract class CommandBase {
    protected logger: Logger = Logger.instance;

    public splitPath(filepath: string, flat: boolean): [string, string] {
        return [
            path.basename(filepath),
            flat ? path.resolve(path.dirname(filepath)) : path.resolve(filepath)
        ];
    }

    protected buildFiles(templates: Array<Template>, { at }: { at: string }): void {
        templates.forEach((template) => {
            const file: File = new File(path.join(at, template.filename));
            file.ensure().writeLines(template.contents);
        });
    }

    protected logDirectoryStructure(dir: string, options?: LogDirStructureOptions) {
        this.logger.log("Directory '" + dir + "':");
        const files = fs.readdirSync(dir)
            .filter((entry) => fs.statSync(path.join(dir, entry)).isFile())
            .sort();

        files.forEach((file) => {
            if(options && options.createdFiles && options.createdFiles.includes(file)) {
                this.logger.success(TAB + file + " << new")
            } else {
                this.logger.log(TAB + file)
            }
        });

        this.logger.log(`${options?.filetype?.capitalize() || "Feature"} '${options?.filename}' was created successfully.`)
    }
}

interface LogDirStructureOptions {
    filename?: string;
    filetype?: string;
    createdFiles?: Array<string>;
}