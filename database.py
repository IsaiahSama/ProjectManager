"""This file will contain the handling for the database"""

from sqlite3 import connect


class Database:
    """Class designed to handle connections and calls to the database.
    
    Attrs:
        DB_NAME (str): The name of the database.
        
    Methods:
        setup(): Used to setup the database."""

    DB_NAME = "projects.sqlite3"

    def __init__(self):
        self.setup()


