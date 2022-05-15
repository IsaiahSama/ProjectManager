import sys
v = sys.version_info
if not (v.major == 3 and v.minor >= 10):
    print("This program requires Python version 3.10 or higher to function. Please update your version of python and try again.")
    input("Press enter to exit")
    raise SystemExit

from mechanics import Menu
import errors

class Main:
    """The main class which handles the main functionality of the program.
    
    Attrs:
        None
    Methods:
        run(): Used to run the program."""

    def __init__(self) -> None:
        self.menu = Menu()

    def run(self):
        while True:
            try:
                self.menu.show_menu()
            except KeyboardInterrupt:
                print("Press enter to return to the main menu. Press ctrl + c again to quit the program.")
                input()
            except errors.MyErrors as err:
                print(err)              

if __name__ == "__main__":
    main = Main()
    main.run()