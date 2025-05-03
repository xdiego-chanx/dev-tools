// #! /usr/bin/env node
import { Command, CommandTree, Named, Positional } from "./cli";

const cli: CommandTree = new CommandTree();

const nest: Command = Command.builder()
    .childOf(CommandTree.root)
    .setName("nest")
    .setHelp("NestJS-related utilities.")
    .build();

const nestResource: Command = Command.builder()
    .childOf(nest)
    .setName("resource")
    .setHelp("Create a NestJS resource, with a controller, service and module.")
    .addArgument(new Positional("path", 0))
    .addArgument(new Named<boolean>("flat", false, "-f"))
    .build()

const nestModule: Command = Command.builder()
    .childOf(nest)
    .setName("module")
    .setHelp("Create a NestJS module file")
    .addArgument(new Positional("path", 0))
    .addArgument(new Named<boolean>("flat", false, "-f"))
    .build()

const nestController: Command = Command.builder()
    .childOf(nest)
    .setName("controller")
    .setHelp("Create a NestJS controller file")
    .addArgument(new Positional("path", 0))
    .addArgument(new Named<boolean>("flat", false, "-f"))
    .build()

const nestService: Command = Command.builder()
    .childOf(nest)
    .setName("service")
    .setHelp("Create a NestJS service file")
    .addArgument(new Positional("path", 0))
    .addArgument(new Named<boolean>("flat", false, "-f"))
    .build()

cli.start();