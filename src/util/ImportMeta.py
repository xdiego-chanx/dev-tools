import os


class ImportMeta:
    __instance: "ImportMeta" = None

    config_path = os.path.abspath(os.path.dirname(__file__), "..", "..", "config.json")

    def __init__(self) -> None:
        if ImportMeta.__instance is not None:
            raise RuntimeError("Use ImportMeta.instance() instead")

    @classmethod
    def instance(cls: type["ImportMeta"]) -> "ImportMeta":
        if cls.__instance is None:
            cls.__instance = ImportMeta()
        return cls.__instance
