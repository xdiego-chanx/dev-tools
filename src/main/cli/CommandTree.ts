import path from "path";
import { Command } from "./Command";

export class CommandTree {
    public static readonly root: Command = new Command(
        path.basename(process.argv[1]),
        "Framework-related utility CLI."
    );

    public start() {
        const args = process.argv.slice(2);
        const next = args[0];
        if (CommandTree.root.subcommands.has(next)) {
            const subcommand = CommandTree.root.subcommands.get(next)!;
            subcommand.parse(args.slice(1));
            return;
        }
    }
}