import { TraverseError } from "@main/error";
import { Positional } from "./positional";
import { Named } from "./named";
import { CommandBuilder } from "./command-builder";
import { Logger } from "@main/lib";

export class Command {
    public logger: Logger = Logger.instance;
    public static NO_OBSERVER = () => Logger.instance.warn("Warning: Command observer not implemented");
    public name: string;
    public help: string;
    public observer: (args: Map<ArgK, ArgV>) => any;

    public positionals: Array<Positional>;
    public named: Array<Named<ArgV>>

    public argumentMap: Map<ArgK, ArgV>;
    public subcommands: Map<string, Command>;

    constructor()
    constructor(name: string, help: string)
    constructor(name: string, help: string, observer: (args: Map<ArgK, ArgV>) => any)
    constructor(name?: string, help?: string, observer?: (args: Map<ArgK, ArgV>) => any) {
        this.name = name ?? "";
        this.help = help ?? "";
        this.observer = observer || Command.NO_OBSERVER;

        this.positionals = [];
        this.named = [];

        this.argumentMap = new Map<ArgK, ArgV>();
        this.subcommands = new Map<string, Command>();
    }

    public static builder(): CommandBuilder {
        return new CommandBuilder();
    }

    public buildHelpString(): string {
        const subcommandsHelp = [...this.subcommands.entries()]
            .map(([name, command]) => `\t${name}: ${command.help}`)
            .join("\n");

        const positionalsHelp = this.positionals
            .map(positional => `    ${positional.name}: ${positional.help}`)
            .join("\n");

        const namedHelp = this.named
            .map(named => {
                const abbr = named.abbr ? ` (${named.abbr})` : "";
                return `    ${named.flag}${abbr}: ${named.help}`;
            })
            .join("\n");


        const help = [
            "Command '" + this.name + "':",
            "",
            "> " + this.help,
            "=".repeat(this.help.length + 2),
            "",
            "Subcommands:",
            subcommandsHelp || " ".repeat(4) + "None",
            "",
            `Arguments:`,
        ];

        if (positionalsHelp.trim()) {
            help.push(positionalsHelp);
        }
        if (namedHelp.trim()) {
            help.push(namedHelp);
        }
        if (!positionalsHelp.trim() && !namedHelp.trim()) {
            help.push(" ".repeat(4) + "None");
        }

        return help.join("\n");
    }

    public traverse(args: Array<string>): void {
        if (args.length == 0) {
            throw new TraverseError("Reached end of branch without finding command.");
        }
        if (args.length >= 2) {
            const next = args[1];
            const subcommand = this.subcommands.get(next);
            if (subcommand) {
                subcommand.traverse(args.slice(1));
            } else {
                this.parse(args.slice(1));
            }
        } else {
            this.parse(args.slice(1));
        }
    }

    public parse(args: string[]): void {
        if (["--help", "-h"].includes(args[0])) {
            if (args.length == 1) {
                this.logger.log(this.buildHelpString());
                return;
            } else {
                throw new TraverseError("Help command takes no additional arguments.")
            }
        }

        this.positionals.sort((a, b) => a.position - b.position);
        this.positionals = this.positionals.map((positional, i) => {
            positional.position = i;
            return positional;
        });


        const passedPositionals = args.slice(0, this.positionals.length);
        const passedNamed = args.slice(this.positionals.length);

        this.positionals.forEach((positional, i) => {
            this.argumentMap.set(positional.name, passedPositionals[i])
        });

        this.named.forEach((named) => {
            const entry = passedNamed.find((arg) => {
                return arg.removeSuffix(/=[\w\-]*/) === named.flag || arg.removeSuffix(/=[\w\-]*/) === named.abbr
            });
            if(!entry) {
                this.argumentMap.set(named.name, named.def);
                return;
            }

            const i = passedNamed.findIndex((arg) => {
                return arg.removeSuffix(/=[\w\-]*/) === named.flag || arg.removeSuffix(/=[\w\-]*/) === named.abbr
            }) + 1;

            let [arg, value]: [string, string] = ["", ""];

            if (entry.indexOf("=") >= 0) {
                [arg, value] = entry.split("=");
            } else if (i < args.length && !this.named.find((arg) => arg.flag === args[i] || arg.abbr === args[i])) {
                [arg, value] = [entry, args[i]]
            }

            switch(typeof named.def) {
                case "string":
                    if (!value) {
                        throw new TypeError("Required argument '" + named.name + "' is missing a value.")
                    }
                    this.argumentMap.set(named.name, value);
                    break;

                case "number":
                    if (!value) {
                        throw new TypeError("Required argument '" + named.name + "' is missing a value.");
                    }
                    if(Number.isNaN(parseFloat(value))) {
                        throw new TypeError("Argument '" + arg + "' expects a number but got 'string'");
                    }
                    this.argumentMap.set(named.name, parseFloat(value));
                    break;
                case "boolean":
                    if(!value) {
                        this.argumentMap.set(named.name, true);
                    } else {
                        if (["true", "on"].includes(value.trim().toLowerCase())) {
                            this.argumentMap.set(named.name, true);
                        } else if (["false", "off"].includes(value.trim().toLowerCase())) {
                            this.argumentMap.set(named.name, false);
                        } else {
                            throw new TypeError("Unknown boolean option '" + value + "'");
                        }
                    }
                    break;
                }
        });

        this.observer(this.argumentMap);
    }
}