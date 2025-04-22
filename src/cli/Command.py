from argparse import _SubParsersAction, ArgumentParser

from src.cli.CommandBuilder import CommandBuilder


class Command:
    __parser = None
    __subparsers = None
    __builder = CommandBuilder()

    def __init__(self, parser: ArgumentParser, final: bool = False, subcommand: str = None) -> None:
        self.__parser = parser
        if not final:
            if subcommand is None:
                raise ValueError("Subcommand name is required for non-final commands")
            self.__subparsers = self.__parser.add_subparsers(dest=subcommand)
        else:
            self.__subparsers = None

    @classmethod
    def builder(self) -> CommandBuilder:
        return self.__builder

    def get_parser(self) -> ArgumentParser:
        return self.__parser

    def get_subparsers(self) -> _SubParsersAction[ArgumentParser]:
        return self.__subparsers
