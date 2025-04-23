from typing import Any


class CommandBuilder:
    __delegate_void = staticmethod(lambda: None)

    def __init__(self):
        self.__final = None
        self.__name = None
        self.__help = None
        # self.__parent = None
        self.__parent_subparsers = None
        self.__string_args = {}
        self.__flags = {}
        self.__handler = self.__delegate_void
    
    def as_child_of(self: "CommandBuilder", command: Any) -> "CommandBuilder":
        self.__parent_subparsers = command.get_subparsers()
        return self
    
    def final(self) -> "CommandBuilder":
        self.__final = True
        return self

    def with_name(self: "CommandBuilder", name: str) -> "CommandBuilder":
        self.__name = name
        return self

    def with_help(self: "CommandBuilder", help: str) -> "CommandBuilder":
        self.__help = help
        return self
    
    def add_string_arg(self: "CommandBuilder", name: str, help: str="", position: int=-1, default: str = None) -> "CommandBuilder":
        if position == -1:
            position = max(self.__string_args.keys(), default=-1) + 1

        if position in self.__string_args:
            raise ValueError(f"Positional argument at position {position} already exists.")
        
        self.__string_args[position] = {
            "name": name,
            "help": help,
            "type": str,
            "required": default is None,
            "default": default
        }

        return self
    
    def add_flag(self: "CommandBuilder", name: str, help: str="", abbr: str="") -> "CommandBuilder":
        if not name.startswith("--"):
            name = f"--{name}"
        if abbr and not abbr.startswith("-"):
            abbr = f"-{abbr}"

        if name in self.__flags:
            raise ValueError(f"Flag '{name}' already exists.")
        
        self.__flags[name] = {
            "name": [name, abbr],
            "help": help
        }
        return self
    
    def set_handler(self: "CommandBuilder", function: callable) -> "CommandBuilder":
        self.__handler = function
        return self

    def build(self: "CommandBuilder") -> Any:
        from src.cli.Command import Command
        if not self.__name:
            raise ValueError("Missing command name")
        if self.__final and self.__handler == self.__delegate_void:
            signature = ", ".join(["str"] * len(self.__string_args) + ["bool"] * len(self.__flags))
            raise ValueError(f"Final command missing command handler 'function({signature})'.")
        if not self.__parent_subparsers:
            raise ValueError("Cannot add a subcommand to a final command.")
        
        parser = self.__parent_subparsers.add_parser(self.__name, help=self.__help)
        parser.set_defaults(func=self.__handler)

        for _, arg in sorted(self.__string_args.items()):
            if arg["required"]:
                parser.add_argument(arg["name"], type=arg["type"], help=arg["help"])
            else:
                parser.add_argument(arg["name"], type=arg["type"], nargs="?", default=arg["default"], help=arg["help"])
        
        for _, arg in self.__flags.items():
            parser.add_argument(*arg["name"], action="store_true", help=arg["help"])

        return Command(parser, self.__final, self.__name)

