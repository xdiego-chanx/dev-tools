import sqlite3


class ConfigureUser:
    
    def __init__(self):
        self.conn = sqlite3.connect("../db.sqlite3")
        self.cursor = self.conn.cursor()

