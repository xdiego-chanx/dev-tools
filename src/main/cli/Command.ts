import { CommandBuilder } from "./CommandBuilder";
import { Named } from "./Named";
import { Positional } from "./Positional";

export class Command {
    public name?: string;
    public abbr?: string;
    public help?: string;
    public subcommands: Map<string, Command>;
    private positionals: Set<Positional>;
    private named: Set<Named<ArgV>>;
    private values: Map<ArgK, ArgV>;

    constructor(
        name?: string,
        help?: string,
        abbr?: string,
        positionals?: Set<Positional>,
        flags?: Set<Named<ArgV>>
    ) {
        this.name = name;
        this.help = help;
        this.abbr = abbr;
        this.subcommands = new Map<string, Command>();
        this.positionals = positionals || new Set<Positional>();
        this.named = flags || new Set<Named<ArgV>>();
        this.values = new Map<ArgK, ArgV>();
    }

    public static builder(): CommandBuilder {
        return new CommandBuilder();
    }

    public parse(args: string[]) {
        const next = args[0]
        if (this.subcommands.has(next)) {
            const subcommand = this.subcommands.get(next)!;
            subcommand.parse(args.slice(1));
            return;
        }

        if (args.length == 1 && ["--help", "-h"].includes(args[0])) {
            console.log(this.help); // TODO implement
            return;
        }
        const positionalArguments = args.slice(0, this.positionals.size);
        const flagArguments = args.slice(this.positionals.size);

        this.positionals.forEach((arg) => {
            this.values.set(arg.name, positionalArguments[arg.position]);
        });

        this.named.forEach((arg) => {
            switch (typeof arg.def) {
                case "boolean":
                    if (args.includes(arg.flag) || (arg.abbr && args.includes(arg.abbr))) {
                        this.values.set(arg.name, true);
                    } else {
                        this.values.set(arg.name, arg.def);
                    }
                    break;
                case "string":
                    if (!args.includes(arg.flag) && (!arg.abbr || !args.includes(arg.abbr))) {
                        this.values.set(arg.name, arg.def);
                    } else {
                        let i: number = -1;

                        if (args.includes(arg.flag)) {
                            i = args.indexOf(arg.flag) + 1;
                        } else if (arg.abbr && args.includes(arg.abbr)) {
                            i = args.indexOf(arg.abbr) + 1;
                        }

                        this.values.set(arg.name, args[i]);
                    }
                    break;
                default:
                    break;
            }
        });

        console.log(this.values);

    }
}