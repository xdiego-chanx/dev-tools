import argparse
from src.cli.Command import Command


class CommandTree:
    app_name = "devtools"
    app_description = "A CLI for framework-related utilties"

    __root = Command(argparse.ArgumentParser(prog=app_name, description=app_description), subcommand="Language or framework")

    def get_root(self: "CommandTree") -> Command:
        return self.__root
    
    def start(self: "CommandTree") -> None:
        args = self.get_root().get_parser().parse_args()
        if hasattr(args, "func"):
            args.func(**vars(args))
        else:
            self.get_root().get_parser().print_help()