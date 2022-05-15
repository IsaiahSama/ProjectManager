"""This file will contain the handling for the database"""

from typing import List, Tuple
from sqlite3 import connect


class Database:
    """Class designed to handle connections and calls to the database.
    
    Attrs:
        DB_NAME (str): The name of the database.
        
    Methods:
        setup(): Used to setup the database.
        query_all_projects(): Used to get all projects from the db.
        query_one_project_by_title(title): Used to get a project by its title.
        add_new_project(title, description, state, comp_date)
        delete_project_by_title(title): Used to delete a project by its title.
        delete_all_projects(): Used to delete all projects stored.
        update_project_by_title(title, new_title, description, state, comp_date): Used to update a project by its title."""

    DB_NAME = "projects.sqlite3"

    def __init__(self):
        self.setup()

    def setup(self):
        """Method used for setting up the database."""
        with connect(self.DB_NAME) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS ProjectTable (
                title TEXT UNIQUE,
                description TEXT,
                state TEXT,
                date_added TEXT,
                comp_date TEXT)""")
            db.commit()

    def query_all_projects(self) -> List[tuple] | None:
        """Method used to retrieve all projects from the database.
        
        Returns:
            list | None"""
        with connect(self.DB_NAME) as db:
            cursor = db.execute("SELECT * FROM ProjectTable")
            rows = cursor.fetchall()
        return rows

    def query_one_project_by_title(self, title:str) -> Tuple | None:
        """Used to retrieve a specific project's information by it's title.
        
        Args:
            title (str): The title of the project. Case insensitive.
            
        Returns:
            Tuple | None"""
        
        with connect(self.DB_NAME) as db:
            cursor = db.execute("SELECT * FROM ProjectTable WHERE title = ?", (title,))
            row = cursor.fetchone()

        return row 

    def add_new_project(self, title:str, description:str, state:str, comp_date:str) -> bool:
        """Adds a new project to the database.
        
        Args:
            title (str): The title of the project.
            description (str): The description of the project.
            state (str): The state of the project.
            comp_date (str): Expected Completion date of the project.
            
        Returns:
            bool"""

        info = (title, description, state, comp_date)

        with connect(self.DB_NAME) as db:
            db.execute("INSERT INTO ProjectTable (title, description, state, comp_date, date_added) VALUES (?, ?, ?, ?, datetime('now', 'localtime'))", info)
            db.commit()

        return True

    def delete_project_by_title(self, title:str):
        """Used to delete a project by it's title
        
        Args:
            title (str): The title of the project to delete."""

        with connect(self.DB_NAME) as db:
            db.execute("DELETE FROM ProjectTable WHERE title=?", (title, ))
            db.commit()
        
        return

    def delete_all_projects(self):
        """Used to delete all projects in the database."""

        with connect(self.DB_NAME) as db:
            db.execute("DELETE FROM ProjectTable")
            db.commit()

    def update_project_by_title(self, title:str, new_title:str=None, description:str=None, state:str=None, comp_date:str=None):
        """Used to update the values of a project.
        
        Args:
            title (str): The title of the project being updated.
            new_title(str): The new title of the project.
            description(str): The new description of the project.
            state (str): The new state of the project.
            comp_date (str): The new completion date of the project."""

        data = ()

        with connect(self.DB_NAME) as db:
            db.execute("""UPDATE ProjectTable 
            SET title = ?,
            description = ?,
            state = ?,
            comp_date = ?
            WHERE title = ?""", data)
            db.commit()



