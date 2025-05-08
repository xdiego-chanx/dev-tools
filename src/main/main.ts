// #! /usr/bin/env node
import { Command, CommandTree, Named, Positional } from "./cli";
import { ConfigCommands } from "./config/config-commands";
import { NestCommands } from "./nest";
import { ReactCommands } from "./react/react-commands";
import { TypescriptCommands } from "./typescript/typescript-commands";

declare global {
    interface String {
        removePrefix: (prefix: string | RegExp) => string;
        removeSuffix: (suffix: string | RegExp) => string;
        isUpperCase: () => boolean;
        isLowerCase: () => boolean;
        capitalize: () => string;
    }

    interface NumberConstructor {
        isDigit: (number: string) => boolean;
    }
}

Number.isDigit = function (str: string): boolean {
    return /^\d$/.test(str);
};

String.prototype.removePrefix = function (prefix: string | RegExp): string {
    if (typeof prefix === "string") {
        return this.startsWith(prefix) ? this.slice(prefix.length) : this.toString();
    } else if (prefix instanceof RegExp) {
        return this.replace(prefix, (match, offset) => (offset === 0 ? "" : match));
    }
    return this.toString();
};

String.prototype.removeSuffix = function (suffix: string | RegExp): string {
    if (typeof suffix === "string") {
        return this.endsWith(suffix) ? this.slice(0, this.length - suffix.length) : this.toString();
    } else if (suffix instanceof RegExp) {
        const match = this.match(suffix);
        if (match && match.index === this.length - match[0].length) {
            return this.slice(0, match.index);
        }
    }
    return this.toString();
};

String.prototype.isUpperCase = function (): boolean {
    return this.toString() === this.toString().toUpperCase();
};

String.prototype.isLowerCase = function (): boolean {
    return this.toString() === this.toString().toLowerCase();
};

String.prototype.capitalize = function (): string {
    return this.charAt(0).toUpperCase() + this.slice(1).toLowerCase();
}


/* Command classes */

// Config Commands
const configCommands: ConfigCommands = new ConfigCommands();

// TypeScript Commands
const typescriptCommands: TypescriptCommands = new TypescriptCommands();

// NestJS Commands
const nestComands: NestCommands = new NestCommands();

// React Commands
const reactCommands: ReactCommands = new ReactCommands();

/* Command tree */

// devtools
const cli: CommandTree = new CommandTree();

// devtools config
const config: Command = Command.builder()
    .childOf(CommandTree.root)
    .setName("config")
    .setHelp("Read or modify the CLI's settings")
    .build();

// devtools config get
const configGet: Command = Command.builder()
    .childOf(config)
    .setName("get")
    .setHelp("Read the value of a config property")
    .addArgument(new Positional("name", "The name (key) of the property to read", 0))
    .setObserver(configCommands.getConfigProperty.bind(configCommands))
    .build();

// devtools config set
const configSet: Command = Command.builder()
    .childOf(config)
    .setName("set")
    .setHelp("Change the value of a config property")
    .addArgument(new Positional("name", "The name (key) of the property to change", 0))
    .addArgument(new Positional("value", "The value to set the property to", 1))
    .setObserver(configCommands.putConfigProperty.bind(configCommands))
    .build();

// devtools config clone
const configClone: Command = Command.builder()
    .childOf(config)
    .setName("clone")
    .setHelp("Clone the config file into the specified path")
    .addArgument(new Positional("path", "The path where the config.json file will be copied into", 0))
    .setObserver(configCommands.getConfigProfile.bind(configCommands))
    .build();

// devtools config override
const configOverride: Command = Command.builder()
    .childOf(config)
    .setName("override")
    .setHelp("Override the current config.json with a config.json file at the specified path")
    .addArgument(new Positional("path", "The path where the overriding config.json file will be found", 0))
    .setObserver(configCommands.putConfigProfile.bind(configCommands))
    .build();

// devtools config explain
const configExplain: Command = Command.builder()
    .childOf(config)
    .setName("explain")
    .setHelp("Prints a tree view of all the config options and a description of what they are and how they're used")
    .setObserver(configCommands.explainConfigOptions.bind(configCommands))
    .build();

// devtools ts
const typescript: Command = Command.builder()
    .childOf(CommandTree.root)
    .setName("ts")
    .setHelp("Typescript-related file and module utilities")
    .build();

// devtools ts class
const typescriptClass: Command = Command.builder()
    .childOf(typescript)
    .setName("class")
    .setHelp("Create a typescript class file")
    .addArgument(new Positional("path", "The path where the file should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified path, without creating a new folder.", false, "-f"))
    .setObserver(typescriptCommands.createClass.bind(typescriptCommands))
    .build();

// devtools ts class
const typescriptInterface: Command = Command.builder()
    .childOf(typescript)
    .setName("interface")
    .setHelp("Create a typescript interface file")
    .addArgument(new Positional("path", "The path where the file should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified path, without creating a new folder.", false, "-f"))
    .setObserver(typescriptCommands.createInterface.bind(typescriptCommands))
    .build();

// devtools ts class
const typescriptEnum: Command = Command.builder()
    .childOf(typescript)
    .setName("enum")
    .setHelp("Create a typescript enum file")
    .addArgument(new Positional("path", "The path where the file should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified path, without creating a new folder.", false, "-f"))
    .setObserver(typescriptCommands.createEnum.bind(typescriptCommands))
    .build();

// devtools ts class
const typescriptBarrel: Command = Command.builder()
    .childOf(typescript)
    .setName("barrel")
    .setHelp("Create a typescript class file")
    .addArgument(new Positional("path", "The path where the file should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified path, without creating a new folder.", false, "-f"))
    .setObserver(typescriptCommands.createBarrel.bind(typescriptCommands))
    .build();

// devtools nest
const nest: Command = Command.builder()
    .childOf(CommandTree.root)
    .setName("nest")
    .setHelp("NestJS-related file and project creation")
    .build();

// devtools nest resource
const nestResource: Command = Command.builder()
    .childOf(nest)
    .setName("resource")
    .setHelp("Create a NestJS resource, containing a module, controller and service")
    .addArgument(new Positional("path", "The path where the resource's files should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create all files in the specified directory, without creating a new folder", false, "-f"))
    .setObserver(nestComands.createResource.bind(nestComands))
    .build();

// devtools nest module
const nestModule: Command = Command.builder()
    .childOf(nest)
    .setName("module")
    .setHelp("Create a NestJS module")
    .addArgument(new Positional("path", "The path where the module file should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified directory, without creating a new folder", false, "-f"))
    .setObserver(nestComands.createModule.bind(nestComands))
    .build();

// devtools nest controller
const nestController: Command = Command.builder()
    .childOf(nest)
    .setName("controller")
    .setHelp("Create a NestJS controller")
    .addArgument(new Positional("path", "The path where the controller file should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified directory, without creating a new folder", false, "-f"))
    .setObserver(nestComands.createController.bind(nestComands))
    .build();

// devtools nest service
const nestService: Command = Command.builder()
    .childOf(nest)
    .setName("service")
    .setHelp("Create a NestJS service")
    .addArgument(new Positional("path", "The path where the service file should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified directory, without creating a new folder", false, "-f"))
    .setObserver(nestComands.createService.bind(nestComands))
    .build();

// devtools nest entity
const nestEntity: Command = Command.builder()
    .childOf(nest)
    .setName("entity")
    .setHelp("Create a NestJS entity")
    .addArgument(new Positional("path", "The path where the entity file should be created. In Prisma's case, specifies the path where schema.prisma should be found or created", 0))
    .addArgument(new Named<boolean>("flat", "Create the file in the specified directory, without creating a new folder", false, "-f"))
    .addArgument(new Named<string>("orm", "The ORM used in the project, whose syntax and modules will be used when creating the entity", "typeorm"))
    .setObserver(nestComands.createEntity.bind(nestComands))
    .build();


cli.start();