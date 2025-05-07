// #! /usr/bin/env node
import { Command, CommandTree, Named, Positional } from "./cli";
import { NestCommands } from "./nest/nest-commands";

const nestCommands: NestCommands = new NestCommands();

const cli: CommandTree = new CommandTree();

const nest: Command = Command.builder()
    .childOf(CommandTree.root)
    .setName("nest")
    .setHelp("NestJS-related utilities.")
    .setObserver(() => undefined)
    .setObserver(() => undefined)
    .build();

const nestResource: Command = Command.builder()
    .childOf(nest)
    .setName("resource")
    .setHelp("Create a NestJS resource with a controller, service and module.")
    .addArgument(new Positional("path", "The path where the resource should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create all files on the specified path, without creating a new folder",  false, "-f"))
    .setObserver(nestCommands.createResource)
    .build();

const nestModule: Command = Command.builder()
    .childOf(nest)
    .setName("module")
    .setHelp("Create a NestJS module file")
    .addArgument(new Positional("path", "The path where the resource should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create all files on the specified path, without creating a new folder",  false, "-f"))
    .setObserver(() => undefined)
    .build();

const nestController: Command = Command.builder()
    .childOf(nest)
    .setName("controller")
    .setHelp("Create a NestJS controller file")
    .addArgument(new Positional("path", "The path where the resource should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create all files on the specified path, without creating a new folder",  false, "-f"))
    .setObserver(() => undefined)
    .build();

const nestService: Command = Command.builder()
    .childOf(nest)
    .setName("service")
    .setHelp("Create a NestJS service file")
    .addArgument(new Positional("path", "The path where the resource should be created", 0))
    .addArgument(new Named<boolean>("flat", "Create all files on the specified path, without creating a new folder",  false, "-f"))
    .setObserver(() => undefined)
    .build();

cli.start();