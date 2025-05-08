import { FileError } from "@main/error/file-error";
import fs from "fs"
import path from "path";

export class File {
    private filepath: string;
    private defaultEncoding: BufferEncoding;
    private content: string;

    constructor(filepath: string, defaultEncoding?: BufferEncoding) {
        this.filepath = path.resolve(filepath);
        this.defaultEncoding =  defaultEncoding || "utf-8";
        this.content = "";
    }

    public get empty(): boolean {
        return this.read().text().length === 0;
    }

    public get dirname(): string {
        return path.dirname(this.filepath);
    }

    public get basename(): string {
        return path.basename(this.filepath);
    }

    public get filename(): string {
        return path.basename(this.filepath).removeSuffix(path.extname(this.filepath));
    }

    public get ext() : string{
        return path.extname(this.filepath).removePrefix(".");
    }

    public get exists(): boolean {
        return fs.existsSync(this.filepath);
    }

    public mkdir(): this {
        const thisdir = path.basename(this.dirname);
        const dirpath = path.dirname(this.dirname);

        if(fs.existsSync(this.dirname)) {
            throw new FileError("Directory '" + this.dirname + "' already exists");
        }

        if(!fs.existsSync(dirpath)) {
            throw new FileError("Create all directories in path '" + dirpath + "' before creating directory '" + thisdir + "'")
        }

        fs.mkdirSync(this.dirname, { recursive: false });
        return this;
    }

    public makedirs(): this {
        if(fs.existsSync(this.dirname)) {
            throw new FileError("Directory '" + this.dirname + "' already exists");
        }

        fs.mkdirSync(this.dirname, { recursive: true });
        return this;
    }

    public ensure(): this {
        fs.mkdirSync(this.dirname, { recursive: true });

        if (!fs.existsSync(this.filepath)) {
            fs.closeSync(fs.openSync(this.filepath, "w"));
        } else {
            const now = new Date();
            fs.utimesSync(this.filepath, now, now);
        }
        return this;
    }

    public touch(): this {
        if (!fs.existsSync(this.dirname)) {
            throw new FileError("Directory '" + this.dirname + "': not found.")
        }

        if (!fs.existsSync(this.filepath)) {
            fs.closeSync(fs.openSync(this.filepath, "w"));
        } else {
            const now = new Date();
            fs.utimesSync(this.filepath, now, now);
        }

        return this;
    }

    public append(data: string | Uint8Array, options?: fs.WriteFileOptions): this {
        if (!fs.existsSync(this.filepath)) {
            throw new FileError("Create file at path '" + this.filepath + "' before appending to it.")
        }

        fs.appendFileSync(this.filepath, data, options);
        this.read();
        return this;
    }

    public write(data: string | NodeJS.ArrayBufferView, options?: fs.WriteFileOptions): this {
        if (!fs.existsSync(this.filepath)) {
            throw new FileError("Create file at path '" + this.filepath + "' before overwriting it.")
        }

        fs.writeFileSync(this.filepath, data, options);
        this.read();
        return this;
    }

    public writeLines(data: string[], options?: fs.WriteFileOptions): this {
        if (!fs.existsSync(this.filepath)) {
            throw new FileError("Create file at path '" + this.filepath + "' before overwriting it.")
        }

        fs.writeFileSync(this.filepath, data.join("\n"), options);
        this.read();
        return this;
    }

    public read(encoding?: BufferEncoding ): this {
        encoding = encoding || this.defaultEncoding;
        if (!this.exists) {
            throw new FileError("Ensure file '" + this.filepath + "' exists before reading to it.");
        }
        this.content =  fs.readFileSync(this.filepath, { encoding });

        return this;
    }

    public text() {
        return this.content;
    }

    public lines() {
        return this.content.split(/\r\n|\r|\n/)
    }
}