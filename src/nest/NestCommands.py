import os
from typing import Self
from src.nest.NestTemplates import NestTemplates
from src.util.Console import Console
from src.util.lib import abortable
from src.util.FileSystem import FileSystem

class NestCommands:
    templates = NestTemplates()
    console = Console.instance()

    @abortable
    def create_feature(self, **kwargs) -> None:
        path = kwargs.get("path")
        no_controller = kwargs.get("no_controller")
        no_service = kwargs.get("no_service")
        no_entity = kwargs.get("no_entity")
        flat = kwargs.get("flat")
        
        path = os.path.abspath(path)
        dirname, filename = FileSystem.split_path(path, flat)

        if not os.path.exists(dirname):
            os.makedirs(path)
        
        templates = list(filter(None, [
            self.templates.module(filename, not no_controller, not no_service),
            self.templates.controller(filename) if not no_controller else None,
            self.templates.service(filename) if not no_service else None,
            self.templates.typeorm_entity(filename) if not no_entity else None # TODO add ORM customization
        ]))

        for template in templates:
            file = FileSystem.touch(os.path.join(dirname, template.filename))
            file.write("\n".join(template.contents))
        self.console.success(self.console.str_created("service", filename, [t.filename for t in templates]))
        return
