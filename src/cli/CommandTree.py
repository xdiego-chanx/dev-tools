import argparse
from src.cli.Command import Command


class CommandTree:
    app_name = "devtools"
    app_description = "A CLI for framework-related utilties"

    __root = Command(argparse.ArgumentParser(prog=app_name, description=app_description), subcommand="Language or framework")

    def get_root(self) -> Command:
        return self.__root