import { TraverseError } from "@main/error";
import { Positional } from "./Positional";
import { Named } from "./Named";
import { CommandBuilder } from "./CommandBuilder";
import { Logger } from "@main/lib";

export class Command {
    public logger: Logger = Logger.instance;
    public static NO_OBSERVER: () => null = () => null;
    public name: string;
    public help: string;
    public observer: (args?: Map<ArgK, ArgV>) => any;

    public positionals: Array<Positional>;
    public named: Array<Named<ArgV>>

    public argumentMap: Map<ArgK, ArgV>;
    public subcommands: Map<string, Command>;

    constructor()
    constructor(name: string, help: string)
    constructor(name: string, help: string, observer: (args?: Map<ArgK, ArgV>) => any)
    constructor(name?: string, help?: string, observer?: (args?: Map<ArgK, ArgV>) => any) {
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
        if(args.length == 0) {
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

    public parse(args: Array<string>) {
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

        const positionalArguments = args.slice(0, this.positionals.length);
        const namedArguments = args.slice(this.positionals.length);

        this.positionals.forEach((positional, i) => {
            this.argumentMap.set(positional.name, positionalArguments[i])
        });

        this.named.forEach((named) => {
            const argument = namedArguments.find((arg) => arg == named.abbr || arg == named.flag);
            if (!argument) {
                return;
            }
            const index = namedArguments.indexOf(argument);

            let key: string | undefined = undefined;
            let value: string | undefined = undefined;

            switch (typeof named.def) {
                case "number":
                    if (argument.includes("=")) {
                        [key, value] = argument.split("=");
                    } else {
                        [key, value] = [argument, namedArguments[index + 1]];
                    }

                    if (!value) {
                        throw new TypeError("Required argument '" + named.name + "' is missing a value.")
                    }

                    if (Number.isNaN(parseFloat(value))) {
                        throw new TypeError("Argument '" + key + "' expects a number. got 'string' instead.");
                    }
                    this.argumentMap.set(named.name, parseFloat(value));
                    break;

                case "string":
                    if (argument.includes("=")) {
                        [key, value] = argument.split("=");
                    } else {
                        [key, value] = [argument, namedArguments[index + 1]];
                    }

                    if (!value) {
                        throw new TypeError("Required argument '" + named.name + "' is missing a value.")
                    }

                    this.argumentMap.set(named.name, value);
                    break;

                case "boolean":
                    if (argument.includes("=")) {
                        [key, value] = argument.split("=");
                    }

                    if (value) {
                        if (["true", "on"].includes(value)) {
                            this.argumentMap.set(named.name, true);
                        } else if (["false", "off"].includes(value)) {
                            this.argumentMap.set(named.name, false);
                        } else {
                            throw new TypeError("Argument '" + key + "' expects a switch (true/false || on/off). got 'string' instead.");
                        }
                    } else {
                        this.argumentMap.set(named.name, true);
                    }
                    break;

                default:
                    throw new TypeError("Argument of type '" + typeof named.def + "' is not assignable to parameter of type 'number | string | boolean'.");
            }
        });

        this.observer(this.argumentMap);
    }
}