import { Argument } from "./Argument";
import { Command } from "./Command";
import { Named } from "./Named";
import { Positional } from "./Positional";

export class CommandBuilder {
    private name!: string;
    private abbr?: string;
    private help!: string;
    private parent!: Command;
    private positionals: Set<Positional> = new Set<Positional>();
    private named: Set<Named<boolean | string>> = new Set<Named<boolean | string>>();

    public childOf(parent: Command): CommandBuilder {
        this.parent = parent;
        return this;
    }

    public setName(name: string): CommandBuilder {
        this.name = name;
        return this;
    }

    public setHelp(help: string): CommandBuilder {
        this.help = help;
        return this;
    } 

    public setAbbr(abbr: string): CommandBuilder {
        this.abbr = abbr;
        return this;
    }

    public addArgument(arg: Argument): CommandBuilder {
        switch(true) {
            case arg instanceof Positional:
                this.positionals.add(arg);
                break;
            case arg instanceof Named:
                this.named.add(arg);
                break;
        }
        return this;
    }


    build(): Command {
        if(!this.name) {
            throw new Error("Command name must be defined before build.");
        }

        if(!this.help) {
            throw new Error("Command help message must be defined before build.");
        }

        if(!this.parent) {
            throw new Error("Non-root command must have a parent.");
        }

        const command = new Command(
            this.name,
            this.help,
            this.abbr,
            this.positionals,
            this.named
        );

        this.parent.subcommands.set(command.name!, command);
        return command;
    }
}