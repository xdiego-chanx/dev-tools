from dataclasses import asdict
import os
from typing import Any

from src.config.ConfigProfile import ConfigProfile
from src.util.FileSystem import FileSystem
from src.util.Console import Console

class ConfigCommands:
    __default_config: dict[str, Any] = asdict(ConfigProfile.default())
    __fs = FileSystem()
    __console: Console = Console()
    __config_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "config.json"))

    def set_config_property(self: "ConfigCommands", name: str, value: str) -> None:
        if name not in self.__default_config:
            self.__console.error(f"'{name}' is not a valid config option.")
            return
        
        if self.__fs.file_exists(self.__config_path):
            config_json: dict[str, Any] = self.__fs.read_json(self.__config_path)
            config_json[name] = value
            self.__fs.write_json(self.__config_path, config_json)
        else: 
            new_config_json = self.__default_config.copy()
            self.__fs.write_json(self.__config_path, new_config_json)

        self.__console.log("Property '{name}' was set to '{value}'")
        return

    def get_config_property(self: "ConfigCommands", name: str) -> Any:
        if name not in self.__default_config:
            self.__console.error(f"'{name}' is not a valid config option.")
            return
        if not self.__fs.file_exists(self.__config_path):
            new_config_json = self.__default_config.copy()
            self.__fs.write_json(self.__config_path, new_config_json)
            self.__console.log(f"'{name}': '{self.__default_config[name]}'")
        return
        
