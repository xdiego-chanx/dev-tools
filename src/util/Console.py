class Console:
    __reset = "\033[0m"
    __white = "\033[97m"
    __cyan = "\033[96m"
    __yellow = "\033[93m"
    __green = "\033[32m"
    __red = "\033[31m"

    def log(self, *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{self.__white}{sep.join(map(str, args))}{self.__reset}", end=end)

    def debug(self, *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{self.__green}{sep.join(map(str, args))}{self.__reset}", end=end)

    def info(self, *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{self.__cyan}{sep.join(map(str, args))}{self.__reset}", end=end)

    def warn(self, *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{self.__yellow}{sep.join(map(str, args))}{self.__reset}", end=end)

    def error(self, *args, sep: str = " ", end: str = "\n") -> None:
        print(f"{self.__red}{sep.join(map(str, args))}{self.__reset}", end=end)

console = Console()
