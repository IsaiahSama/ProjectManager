"""File which will contain my custom errors for the sole purpose of the fact that I can :)"""


class MyErrors(Exception):
    """Base class for me Exceptions."""

    def __init__(self, *args):
        result = ', '.join(args)
        super().__init__(result)


class MissingEntryError(MyErrors):
    """Exception raised when a queried database entry does not exist."""

    def __init__(self, *args):
        base_message = "MissingEntryError: A value that you queried does not exist in the database."
        result = ', '.join([base_message, *args])
        super().__init__(result)

class DuplicateEntryError(MyErrors):
    """Exception raised when an entry with a given title already exists."""

    def __init__(self, *args):
        base_message = "DuplicateEntryError: Entry with this name already exists."
        result = ', '.join([base_message, *args])
        super().__init__(result)