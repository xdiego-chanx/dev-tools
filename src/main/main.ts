// #! /usr/bin/env node
import { Command, CommandTree, Flag, Positional } from "./cli";

const cli: CommandTree = new CommandTree();

const nest: Command = Command.builder()
    .childOf(CommandTree.root)
    .setName("nest")
    .setHelp("NestJS-related utilities.")
    .addArgument(new Positional("name", 0))
    .addArgument(new Positional("path", 1))
    .addArgument(new Flag("flat", "-f"))
    .build();

cli.start();