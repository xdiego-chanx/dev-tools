import json
from json import JSONDecodeError
import os
import time
from typing import Any, TextIO

class FileSystem:

    @classmethod
    def split_path(cls: type["FileSystem"], path: str, flat: bool) -> tuple[str, str]:
        if flat:
            return (os.path.abspath(os.path.dirname(path)), os.path.basename(path))
        else:
            return (os.path.abspath(path), os.path.basename(path))

    @classmethod
    def touch(cls: type["FileSystem"], path: str) -> TextIO:
        path = os.path.abspath(path)

        if os.path.exists(path) and not os.path.isfile(path):
            raise ValueError(f"Path '{path}' already exists and is not a valid file path.")
        
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8"):
                pass 

        now = time.time()
        os.utime(path, (now, now))

        return open(path, "r+", encoding="utf-8")
    
    @classmethod
    def file_exists(cls: type["FileSystem"], path: str) -> bool:
        return os.path.exists(path) and os.path.isfile(path)
    
    @classmethod
    def read_json(cls: type["FileSystem"], path: str) -> dict[str, Any]:
        path = os.path.abspath(path)

        if not os.path.exists(path) or not os.path.isfile(path):
            raise ValueError(f"Path '{path}' is not a valid file path.")
        
        if os.path.splitext(path)[1] != ".json":
            raise ValueError(f"Path '{path}' does not resolve to a valid JSON file")
        
        with open(path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except JSONDecodeError:
                if not file.read():
                    return None
                raise ValueError(f"File '{path}' does not contain valid JSON.")
    
    @classmethod 
    def write_json(cls: type["FileSystem"], path: str, contents: dict[str, Any]) -> None:
        path = os.path.abspath(path)

        if os.path.exists(path) and not os.path.isfile(path):
            raise ValueError(f"Path '{path}' already exists and is not a valid JSON file.")
        
        file: TextIO = FileSystem.touch(path)

        file.write(json.dumps(contents, indent=4))

