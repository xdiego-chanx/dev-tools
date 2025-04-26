from src.util.Console import Console


def abortable(func: callable) -> callable:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            Console.instance().error("Operation aborted")
            return
    return wrapper
