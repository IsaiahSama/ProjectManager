"""File which will contain my custom errors for the sole purpose of the fact that I can :)"""

class MissingEntryError(Exception):
    """Exception raised when a queried database entry does not exist."""

    def __init__(self, *args):
        base_message = "MissingEntryError: A value that you queried does not exist in the database."
        super().__init__(base_message, args)

class DuplicateEntryError(Exception):
    """Exception raised when an entry with a given title already exists."""

    def __init__(self, *args):
        base_message = "DuplicateEntryError: Entry with this name already exists."
        super().__init__(base_message, args)