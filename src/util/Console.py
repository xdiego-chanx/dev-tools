class Console:
    __reset = "\033[0m"
    __gray = "\033[90m"
    __white = "\033[97m"
    __cyan = "\033[96m"
    __yellow = "\033[93m"
    __green = "\033[32m"
    __red = "\033[31m"

    __instance: "Console" = None

    def __init__(self) -> None:
        if Console.__instance is not None:
            raise RuntimeError("Use Console.instance() instead")
    
    @classmethod
    def str_created(cls: type["Console"], ft: str, name: str, files: list[str]) -> str:
        return f"{ft.capitalize()} '{name}' was created with files '{"', '".join(files)}'."

    @classmethod
    def instance(cls: type["Console"]) -> "Console":
        if cls.__instance is None:
            cls.__instance = Console()
        return cls.__instance

    @classmethod
    def log(cls: type["Console"], *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{cls.__white}{sep.join(map(str, args))}{cls.__reset}", end=end)

    @classmethod
    def log(cls: type["Console"], *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{cls.__gray}{sep.join(map(str, args))}{cls.__reset}", end=end)
    @classmethod
    def success(cls: type["Console"], *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{cls.__green}{sep.join(map(str, args))}{cls.__reset}", end=end)

    @classmethod
    def info(cls: type["Console"], *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{cls.__cyan}{sep.join(map(str, args))}{cls.__reset}", end=end)

    @classmethod
    def warn(cls: type["Console"], *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{cls.__yellow}{sep.join(map(str, args))}{cls.__reset}", end=end)

    @classmethod
    def error(cls: type["Console"], *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{cls.__red}{sep.join(map(str, args))}{cls.__reset}", end=end)
