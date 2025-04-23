from dataclasses import asdict
from src.config.ConfigProfile import ConfigProfile
from src.util.FileSystem import FileSystem
from src.util.ImportMeta import ImportMeta


class ConfigRules:
    meta: ImportMeta
    default_config = ConfigProfile.default()
    config: ConfigProfile

    quotes: str
    indent: str
    semicolon: str
    bracket_space: str
    eol: str
    trailing_comma: str
    obj_space: str


    def __init__(self):
        self.meta = ImportMeta.instance()
        config_dict = FileSystem.read_json(self.meta.config_path) or asdict(ConfigProfile.default())
        self.config = ConfigProfile(**config_dict)

        # quotes
        if self.config.quotes == "smart":
            pass # create language profiles
        elif self.config.quotes == "double":
            self.quotes = '"'
        elif self.config.quotes == "single":
            self.quotes = "'"

        # tab width (only for space)
        tab_width = self.default_config.tab_width if self.config.tab_width <= 0 else self.config.tab_width

        # indent style
        if self.config.indent == "tab":
            self.indent = "\t"
        elif self.config.indent == "space":
            self.indent = " " * tab_width
        
        # bracket spacing
        if self.config.bracket_spacing == "smart":
            pass # create language profiles
        elif self.config.bracket_spacing == "tight":
            self.bracket_space = ""
        elif self.config.bracket_spacing == "space":
            self.bracket_space = " "
        elif self.config.bracket_spacing == "newline":
            self.bracket_space = "\n"
        
        # EOL sequence
        if self.config.eol == "cr":
            self.eol = "\r"
        elif self.config.eol == "lf":
            self.eol = "\n"
        elif self.config.eol == "crlf":
            self.eol = "\r\n"

        self.semicolon = ";" if self.config.semicolon else ""
        self.trailing_comma = "," if self.config.trailing_comma else ""
        self.obj_space = " " if self.config.spaced_objects else ""
        
