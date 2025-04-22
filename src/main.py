import argparse
from src.cli.CommandTree import CommandTree
from src.cli.Command import Command


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


def main():
    cli = CommandTree()

    settings = (
        Command.builder()
        .as_child_of(cli.get_root())
        .with_name("settings")
        .with_help("Read or modify the CLI's settings.")
        .build()
    )

    settings_set = (
        Command.builder()
        .final()
        .as_child_of(settings)
        .with_name("set")
        .with_help("Change a setting by changing its value")
        .add_string_arg("name", help="The name of the setting to modify")
        .add_string_arg("value", help="The new value for the setting")
        .set_handler()
        .build()
    )

    settings_get = (
        Command.builder()
        .final()
        .as_child_of(settings)
        .with_name("get")
        .with_help("Retrieve a setting and print it to the console")
        .add_string_arg("name", help="The name of the setting to retrieve")
        .set_handler()
        .build()
    )


if __name__ == "__main__":
    main()
