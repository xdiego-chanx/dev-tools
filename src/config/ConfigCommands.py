from dataclasses import asdict
from typing import Any

from src.config.ConfigProfile import ConfigProfile
from src.util.ImportMeta import ImportMeta
from src.util.FileSystem import FileSystem
from src.util.Console import Console

class ConfigCommands:
    __default_config: dict[str, Any] = asdict(ConfigProfile.default())

    meta = ImportMeta.instance()
    console = Console.instance()

    def set_config_property(self: type["ConfigCommands"], **kwargs) -> None:
        try:
            name = str(kwargs.get("name"))
            value = str(kwargs.get("value"))
        except KeyError:
            self.console.error("Required arguments 'name' and 'value' incorrectly passed to handler.")
            return

        if name not in self.__default_config:
            self.console.error(f"'{name}' is not a valid config option.")
            return
        
        if FileSystem.file_exists(self.meta.config_path):
            config_json: dict[str, Any] = FileSystem.read_json(self.meta.config_path) or self.__default_config.copy()
        else: 
            config_json = self.__default_config.copy()

        default_value = self.__default_config[name]

        if isinstance(default_value, int):
            value = int(value)
        elif isinstance(default_value, float):
            value = float(value)
        elif isinstance(default_value, bool):
            value = not not value
        else:
            value = str(value)

        if config_json[name] == value:
            self.console.log(f"Property '{name}' already has a value of '{value}'")
            return

        config_json[name] = value
        FileSystem.write_json(self.meta.config_path, config_json)

        self.console.log(f"Property '{name}' was set to '{value}'")
        return

    def get_config_property(self: type["ConfigCommands"], **kwargs) -> None:
        try:
            name = str(kwargs.get("name"))
        except KeyError:
            self.console.error("Required argument 'name' incorrectly passed to handler.")
            return
        
        if name not in self.__default_config:
            self.console.error(f"'{name}' is not a valid config option.")
            return
        
        if FileSystem.file_exists(self.meta.config_path):
            config_json = FileSystem.read_json(self.meta.config_path)
            if not config_json:
                config_json = self.__default_config.copy()
                FileSystem.write_json(self.meta.config_path, config_json)
        else:
            config_json = self.__default_config.copy()
            FileSystem.write_json(self.meta.config_path, config_json)
        
        value = config_json[name]

        if isinstance(value, str):
            value = f"'{value}'"
        if isinstance(value, bool):
            value = str(value).lower()

        self.console.log(f"{name}: {value}")
        return
        
