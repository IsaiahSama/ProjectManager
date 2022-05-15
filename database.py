"""This file will contain the handling for the database"""
import errors

from typing import List, Tuple
from sqlite3 import connect


class Database:
    """Class designed to handle connections and calls to the database.
    
    Attrs:
        DB_NAME (str): The name of the database.
        
    Methods:
        setup(): Used to setup the database.
        query_all_projects(): Used to get all projects from the db.
        query_project_by_title(title): Used to get a project by its title.
        query_project_titles(): Used to get all titles of projects
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
            list | None
            
        Raises: 
            MissingEntryError"""

        with connect(self.DB_NAME) as db:
            cursor = db.execute("SELECT * FROM ProjectTable")
            rows = cursor.fetchall()

        if not rows: raise errors.MissingEntryError("No entries have been made as yet.")
        return rows

    def query_project_by_title(self, title:str) -> Tuple | None:
        """Used to retrieve a specific project's information by it's title.
        
        Args:
            title (str): The title of the project. Case insensitive.
            
        Returns:
            Tuple | None
            
        Raises:
            MissingEntryErrorr"""
        
        with connect(self.DB_NAME) as db:
            cursor = db.execute("SELECT * FROM ProjectTable WHERE title = ?", (title,))
            row = cursor.fetchone()

        if not row: raise errors.MissingEntryError("No entry with the title ", title, " exists")

        return row 

    def query_project_titles(self) -> List | None:
        """Used to get all the titles of projects.
        
        Returns:
            List | None"""

        rows = self.query_all_projects()
        titles = [row[0] for row in rows]
        return titles

    def add_new_project(self, title:str, description:str, state:str, comp_date:str) -> bool:
        """Adds a new project to the database.
        
        Args:
            title (str): The title of the project.
            description (str): The description of the project.
            state (str): The state of the project.
            comp_date (str): Expected Completion date of the project.
            
        Returns:
            bool
            
        Raises:
            DuplicateEntryError"""

        info = (title, description, state, comp_date)

        try:
            self.query_project_by_title(title)
        except errors.MissingEntryError:
            pass
        else:
            raise errors.DuplicateEntryError("Name: ", title)

        with connect(self.DB_NAME) as db:
            db.execute("INSERT INTO ProjectTable (title, description, state, comp_date, date_added) VALUES (?, ?, ?, ?, datetime('now', 'localtime'))", info)
            db.commit()

        return True

    def delete_project_by_title(self, title:str):
        """Used to delete a project by it's title
        
        Args:
            title (str): The title of the project to delete.
            
        Raises:
            MissingEntryError"""


        try:
            self.query_project_by_title(title)
        except errors.MissingEntryError:
            raise errors.MissingEntryError("Cannot delete nonexistent entry with title ", title)

        with connect(self.DB_NAME) as db:
            db.execute("DELETE FROM ProjectTable WHERE title=?", (title, ))
            db.commit()
        
        return

    def delete_all_projects(self):
        """Used to delete all projects in the database.
        
        Raises:
            If no entry exists, will raise MissingEntryError"""

        self.query_all_projects()

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
            comp_date (str): The new completion date of the project.
            
        Raises:
            If project does not exist, will raise MissingEntryError."""

        # May raise MissingEntryError
        og = self.query_project_by_title(title)

        data = list(og)[:-1]
        
        if new_title:
            data[0] = new_title
        if description:
            data[1] = description
        if state:
            data[2] = state
        if comp_date:
            data[3] = comp_date
        

        with connect(self.DB_NAME) as db:
            db.execute("""UPDATE ProjectTable 
            SET title = ?,
            description = ?,
            state = ?,
            comp_date = ?
            WHERE 
            title = ?""", (*data, title))
            db.commit()


if __name__ == "__main__":
    db = Database()
