""" 
    Summary:
        Main module of the application  , this module is the entry point of the application 
"""

import typer
from config.config_manager import ConfigManager
from menus.main_menu import MainMenu
from scripts.file_organizer import FileOrganizer

def main():
    """ Summary: 
            Main function of the application        
    """
    config_manager = ConfigManager()
    main_menu = MainMenu(config_manager)
    file_organizer = FileOrganizer(config_manager)

    while True:
        main_menu.display()
        choice = main_menu.handle_input()
        if choice == "run_organizer":
            file_organizer.run()
        elif choice == "exit":
            break


if __name__ == "__main__":
    typer.run(main)
