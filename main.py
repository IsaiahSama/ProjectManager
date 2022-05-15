import sys
v = sys.version_info
if not (v.major == 3 and v.minor >= 10):
    print("This program requires Python version 3.10 or higher to function. Please update your version of python and try again.")
    input("Press enter to exit")
    raise SystemExit

class Main:
    """The main class which handles the main functionality of the program.
    
    Attrs:
        None
    Methods:
        run(): Used to run the program."""

    def run(self):
        pass

    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    main = Main()
    main.run()