import path from "path";
import { Command } from "./Command";

export class CommandTree {
    public static readonly root: Command = new Command(
        path.basename(process.argv[1]),
        "Framework-related utility CLI."
    );

    public start() {
        CommandTree.root.traverse(process.argv.slice(1));
    }
}