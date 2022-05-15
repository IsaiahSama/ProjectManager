"""Will contain all of the mechanics used by the program."""

import database
import errors


db = database.Database

class Validator:
    """Class used to validate input
    
    Attrs:
        None
        
    Methods:
        validate_title(title): Used to validate a given title.
        validate_yes_no(prompt:str): Used to validate a yes, no response."""

    def __init__(self) -> None:
        pass

    def validate_title(self, title:str) -> bool:
        """Used to validate a title.
        
        Args:
            title(str): The title to be validated.
        
        Returns:
            bool"""

        try:
            db.query_project_by_title(title)
        except errors.MissingEntryError:
            return False
        return True

    def validate_yes_no(self, prompt:str) -> bool:
        """Used to validate a yes no response.
        
        Args:
            prompt (str): The prompt to be displayed.
            
        Returns:
            bool"""

        print(prompt)
        print("Yes or No?")
        response = input(": ")

        return response.lower().startswith("y")

class Menu:
    """The main menu of the program.
    
    Attrs:
        None
        
    Methods:
        None"""

    def __init__(self) -> None:
        pass