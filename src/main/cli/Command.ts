import { CommandBuilder } from "./CommandBuilder";
import { Flag } from "./Flag";
import { Positional } from "./Positional";

export class Command {
    public name?: string;
    public abbr?: string;
    public help?: string;
    public subcommands: Map<string, Command>;
    private positionals: Set<Positional>;
    private flags: Set<Flag>;
    private values: Map<string | number, string>;

    constructor(name?: string, help?: string, abbr?: string, positionals?: Set<Positional>, flags?: Set<Flag>) {
        this.name = name;
        this.help = help;
        this.abbr = abbr;
        this.subcommands = new Map<string, Command>();
        this.positionals = positionals || new Set<Positional>();
        this.flags = flags || new Set<Flag>();
        this.values = new Map<string | number, string>();
    }

    public static builder(): CommandBuilder {
        return new CommandBuilder();
    }

    public parse(args: string[]) {
        if(args.length == 1 && ["--help", "-h"].includes(args[0])) {
            console.log(this.help);
            return;
        }
        const positionalArguments = args.slice(0, this.positionals.size);
        const flagArguments = args.slice(this.positionals.size);

        this.positionals.forEach((arg) => {
            this.values.set(arg.name, positionalArguments[arg.position]);
        });

        console.log(this.values);
        console.log(flagArguments);
    }
}