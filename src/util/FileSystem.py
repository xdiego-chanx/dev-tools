import json
from json import JSONDecodeError
import os
import time
from typing import IO, Any

class FileSystem:

    @classmethod
    def touch(cls: "FileSystem", path: str) -> IO[Any]:
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
    def read_json(cls: "FileSystem", path: str) -> dict[str, Any]:
        path = os.path.abspath(path)

        if not os.path.exists(path) or not os.path.isfile(path):
            raise ValueError(f"Path '{path}' is not a valid file path.")
        
        if os.path.splitext(path)[1] != ".json":
            raise ValueError(f"Path '{path}' does not resolve to a valid JSON file")
        
        with open(path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except JSONDecodeError:
                raise ValueError(f"File '{path}' does not contain valid JSON.")
            
fs = FileSystem()
