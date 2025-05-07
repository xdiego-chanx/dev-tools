import { interruptible, requires } from "@main/lib/decorators";
import path from "path";

export class NestCommands {
    
    @interruptible()
    @requires("path")
    @requires("flat")
    public createResource(args: Map<ArgK, ArgV>): void {
        const relpath: string = args.get("path") as string;
        const flat: boolean = args.get("flat") as boolean;

        console.log(relpath);
        console.log(flat)

        const abspath: string = path.resolve(relpath);
    }
}