"""Will contain all of the mechanics used by the program."""

import database
import errors


db = database.Database()

class Beautify:
    """Class used to format stuff... I guess??
    
    Attrs:
        None
        
    Methods:
        format_menu(menu_dict): Formats the menu.
        format_project(info:tuple): Formats projectt information."""

    def __init__(self) -> None:
        pass

    def format_menu(self, menu_dict: dict) -> str:
        """Used to format the menu.
        
        Args:
            menu_dict (dict): The dictionary of the menu.
            
        Returns:
            str"""

        output = ""
        for index, key in enumerate(menu_dict, start=1):
            output += index + ") " + key + "\n"

        return output

    def format_project(self, details:tuple) -> str:
        """Used to format project information."""

        return f"Title: {details[0]}\nDescription: {details[1]}\nState: {details[2]}\nDate Added: {details[3]}\nETA: {details[4]}\n"

class Validator:
    """Class used to validate input
    
    Attrs:
        None
        
    Methods:
        validate_title(title): Used to validate a given title.
        validate_yes_no(prompt:str): Used to validate a yes, no response.
        validate_choice(prompt:str, options:dict): Used to validate a choice."""

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

    def validate_choice(self, prompt:str, options:dict) -> str:
        """Used to validate a choice.
        
        Args:
            prompt (Str): The prompt to be displayed to the user.
            options (dict): Dict mapping option to value.
            
        Returns:
            str (Valid Input)"""
        
        print(prompt)
        while True:
            resp = input(": ")
            if resp not in options: 
                print("Invalid choice.")
                continue
            break
        return options[resp]

class Menu:
    """The main menu of the program.
    
    Attrs:
        menu_options (dict): A dictionary of menu options.
        
    Methods:
        show_menu(): Used to display the menu to the user.
        add_project(): Used to add a new project.
        update_project(): Used to update a project.
        view_project(): Used to view a project.
        delete_project(): Used to delete a project."""

    def __init__(self) -> None:
        self.beauty = Beautify()
        self.validate = Validator()

        self.menu_options = {
            "Add New Project": self.add_project,
            "Update Project": self.update_project,
            "View Project": self.view_project,
            "Delete Project": self.delete_project
        }

        self.states = {
            "1": "To Do",
            "2": "In Progress",
            "3": "Dropped",
            "4": "Completed"
        }

    def fix(self, e):
        e = list(e)
        e[0] = str(e[0])
        return tuple(e)

    def optionify(self, items:list):
        return dict([self.fix(e) for e in list(enumerate(items, start=1))])

    def show_menu(self):
        """Used to display the menu to the user."""

        options = self.optionify(self.menu_options)
        menu = self.beauty.format_menu(self.menu_options)

        message = "Select the number of the option you want to do.\n"
        choice = self.validate.validate_choice(message + menu, options)

        self.menu_options[choice]()

    def add_project(self):
        """Used to add a new project."""
        print("Press ctrl + c at any time to quit")
        while True:
            print("What is the title for this project?")
            title = input(": ")
            if self.validate.validate_title(title): break
            else: print("This title already exists for a project.")
        
        while True:
            print("Give me a brief description for this project. Keep it to one line.")
            desc = input(": ")
            if self.validate.validate_yes_no("Is this description fine?"): break
            else: print("Ok, again.")

        while True:
            state = self.validate.validate_choice("What state is the project in? Select the matching number from the below options", self.states)
            if self.validate.validate_yes_no("Are you sure you want to set the state to " + state + "?"): break
            else: print("Ok, again.")

        while True:
            print("When do you expect to complete this project?")
            eta = input(": ")
            if self.validate.validate_yes_no("Are you sure this is what you want?"): break
            else: print("Alright. Again.")
        
        message = f"Title: {title}\nDescription: {desc}\nState: {state}\nETA: {eta}\n"
        if not self.validate.validate_yes_no("Is all of the information correct?\n\n" + message):
            print("Returning to main menu.")
            return False

        print("Understood. Saving~")
        
        db.add_new_project(title, desc, state, eta)
        print("Completed")

    def update_project(self):
        """Used to update a project."""
        pass 

    def view_project(self, title:str=None) -> str:
        """Used to view a project.
        
        Args:
            title (str): The title of the project to view.
            
        Returns:
            Str: The selected title"""

        if title:
            target = title

        if not target:
            options = self.optionify(db.query_project_titles())
            target = self.validate.validate_choice("Which project do you want to view? Select the number that matches the name.", options)

        print(self.beauty.format_project(db.query_project_by_title(target)))
        input("Press enter to continue")

        return target 

    def delete_project(self):
        """Used to delete a project."""
        print("What project do you want to delete?")
        title = self.view_project()
        
        if self.validate.validate_yes_no("Are you sure you want to delete this project?"):
            db.delete_project_by_title(title)
