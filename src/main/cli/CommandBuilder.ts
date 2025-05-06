import { BuilderError } from "@main/error";
import { Command } from "./Command";
import { Named } from "./Named";
import { Positional } from "./Positional";
import { Argument } from "./Argument";

export class CommandBuilder {
    private command: Command;
    private parent!: Command;

    constructor() {
        this.command = new Command();
    }
    
    public childOf(command: Command): CommandBuilder {
        this.parent = command;
        return this;
    }

    public setName(name: string): CommandBuilder {
        this.command.name = name;
        return this;
    }

    public setHelp(help: string): CommandBuilder {
        this.command.help = help;
        return this;
    }

    public setObserver(observer: (args?: Map<ArgK, ArgV>) => any): CommandBuilder {
        this.command.observer = observer;
        return this;
    }
    

    public addArgument(arg: Argument): CommandBuilder {
        switch (true) {
            case arg instanceof Positional:
                this.command.positionals.push(arg);
                break;
            case arg instanceof Named:
                this.command.named.push(arg);
                break;
            default:
                throw new BuilderError("Unknown argument type");
        }

        return this;
    }

    public build(): Command {
        if(!this.parent) {
            throw new BuilderError("Non-root command must have a parent")
        }
        if(!this.command.name) {
            throw new BuilderError("Required property 'name' is missing a value");
        }
        if (this.parent.subcommands.has(this.command.name)) {
            throw new BuilderError(`Subcommand '${this.command.name}' is already part of '${this.parent.name}'`);
        } 
        if(!this.command.help) {
            throw new BuilderError("Required property 'help' is missing a value");
        }

        if(this.command.observer === Command.NO_OBSERVER) {
            throw new BuilderError("Required property 'observer' is missing a value")
        }

        this.command.named.push(new Named("help", "Get information about the current command", false, "-h"));

        this.parent.subcommands.set(this.command.name, this.command);

        return this.command;
    }
}
