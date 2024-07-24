"""
    #! Descripción Deprecated --- > Ahora la idea es expandir a mas scripts \\
    #? no solo organizar archivos

    Modulo para organizar los archivos en carpetas específicas
    según su extensión y categoría.

    El script se encarga de organizar los archivos descargados en carpetas
    específicas según su extensión y categoría. El script se ejecuta en segundo
    plano y monitorea la carpeta de descargas para mover los archivos a las
    carpetas correspondientes.

"""
# ? pip install -r requirements.txt
import json  # Para cargar el archivo de configuración y guardar las Rutas y extensiones
import os  # Para todo lo relacionado con el sistema operativo
import re  # Para limpiar el path de los archivos
import time  # Para medir tiempo de ejecución y dar tiempo al usuario para leer mensajes
import shutil  # Para mover los archivos a las carpetas correspondientes
from pathlib import Path  # Para trabajar con los objetos Path
# Para seleccionar la carpeta donde se organizarán los archivos
from tkinter import filedialog
from typing import Any, Dict, List, Tuple  # Type Hints
import typer  # Para crear la interfaz de línea de comandos  #* pip install typer
from rich import print as rprint  # Cool rprint statements #* pip install rich
from rich.table import Table  # Cool tables


# * Configuración de la interfaz de línea de comandos

# Prompt Aliases [ to reduce code  ]

# * Input Aliases
ARROWLINE: str = "\n┈┈┈┈┈┈┈┈┈┈┈┈➣ Ingrese una opción: "
ARROW: str = "\n┈┈┈┈┈┈┈┈┈┈┈┈➣"
DEFAULT_ERROR: str = "\n┈┈┈┈┈┈┈┈┈┈┈┈➣ Opción inválida. Intente nuevamente."
EXIT: str = f"\n{ARROW} Saliendo del script... "

# * Output Aliases Default
LINE_R: str = "[bold blue]╌╌╌╌╌╌╌╌╌╌╌[/bold blue]"  # ? ────────── Extra Line 1
LINE_L: str = "[bold blue]╌╌╌╌╌╌╌╌╌╌╌[/bold blue]"  # ? ‐‐‐‐‐‐‐‐‐‐ Extra Line 2
ARROW_R: str = ">"  # ? ⇾ Extra Right arrow
ARROW_L: str = "<"  # ? ⇽  Extra Left arrow
ARROW_LINE_RIGHT: str = f"{LINE_R}{ARROW_R}"
ARROW_LINE_LEFT: str = f"{ARROW_L}{LINE_L}"
ERROR: str = "[bold orange_red1]Error[/bold orange_red1]"
REGRESAR_MENU: str = "[bold yellow]Regresar al menú principal[/bold yellow]"
SALIR: str = "[bold orange_red1]Salir[/bold orange_red1]"
DESCRIPTION_TEXT: str = "Descripción"
CANCELED_OPERATION: str = "[bold yellow]Operación cancelada[/bold yellow]"

# * Output Aliases Extra - Future Implementation
# ENVOLVER_ARRIBA: str = "╭─────────────────────────────────────────────────────────────────────────────────────╮"
# ENVOLVER_ABAJOO: str = "╰─────────────────────────────────────────────────────────────────────────────────────╯"

# * Global Variables

# Global variables - Config file
CONFIG_FILE: str = "config.json"
config: Dict = {}

# Global variables - Paths and Extensions
paths_dict: Dict = {}
main_paths: Dict = {}
all_extensions: List = []
sub_paths: Dict = {}
extensions_by_category: Dict = {}
exceptions: Dict = {}
main_paths_str: Dict = {}

# Global variables - OS and User Related
os_name: str = ""
user_name: str = ""
full_path: Path
target_path: Path
full_path_str: str = ""
target_path_str: str = ""

# Global variables - Organize files
carpetas_revisadas: List[str] = []
archivos_a_organizar: List = []
archivos_dentro_de_excepciones: List = []

# Global Testing variables
# test_exception_path: str = "C:\\Program Files"


# * Yuu Tools Setup


def create_config() -> Dict:
    """
        Summary:
            Create the config.json file if don't exist 

        Returns:
            Dict: Returns the configuration file created
    """
    if not os.path.exists(CONFIG_FILE):
        config = {
            "OS": "Windows",
            "User": "YuzuTest",
            "TargetPath": "System32",
            "FullPath": "C:\\Windows\\System32",
            "Paths": {
                "Images": {
                    "Path": "",
                    "Extensions": ["PNG", "JPG", "JPEG", "GIF", "SVG"],
                    "Subrutas": {}
                },
                "Videos": {
                    "Path": "",
                    "Extensions": ["MP4", "MKV", "AVI", "MOV", "WMV"],
                    "Subrutas": {}
                },
                "Documents": {
                    "Path": "",
                    "Extensions": ["PDF", "DOCX", "DOC", "XLSX", "XLS", "PPTX", "PPT", "TXT"],
                    "Subrutas": {}
                },
                "Music": {
                    "Path": "",
                    "Extensions": ["MP3", "WAV", "FLAC", "M4A", "AAC"],
                    "Subrutas": {}
                },
                "Compressed": {
                    "Path": "",
                    "Extensions": ["ZIP", "RAR", "7Z"],
                    "Subrutas": {}
                },
                "Programs": {
                    "Path": "",
                    "Extensions": ["EXE", "MSI"],
                    "Subrutas": {}
                }
            },
            "Excepciones": {
                "La carpeta Tarea": "",
            }
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)
    return config


def load_config() -> Dict:
    """
        Summary:
            Load the configuration file from the config.json file into the script

        Returns:
            Dict: Returns the configuration file loaded
    """
    try:
        # Get the current directory path
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path of the JSON file
        config_file = os.path.join(current_dir, CONFIG_FILE)
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                global config
                config = json.load(file)
        except FileNotFoundError:
            rprint(f"{ARROW} {
                   ERROR} al buscar el archivo de configuración, [bold hot_pink]config.json[/bold hot_pink] no [bold orange_red1]existe[/bold orange_red1]")
            create_file = typer.confirm(
                f"{ARROW} ¿Desea crear un archivo de configuración nuevo?")
            if create_file:
                rprint(
                    f"{ARROW} Luego de crear el [bold hot_pink]config.json[/bold hot_pink], vuelva a ejecutar el script")
                rprint(
                    f"{ARROW} Recuerde modificar las rutas desde este mismo script antes de empezar a organizar archivos")
                rprint(f"\n{ARROW} Creando archivo de configuración...")
                create_config()
                clear_screen()
                rprint(
                    f"{ARROW} Archivo de configuración básico creado [bold green]exitosamente[/bold green]")
                exit()
    except OSError as e:
        rprint(f"{ARROW} {ERROR} {e}")
        rprint(f"{ARROW} {ERROR} al cargar el archivo de configuración")
        exit()
    return config


def return_main_menu() -> str:
    """
        Summary:
            Return to the main menu

        Returns: 
            str: Returns the prompt to the main menu        
    """
    rprint(f"{ARROW} Regresando al menú principal...")
    main_menu()
    return __prompt_main__()


def load_data_from_config() -> tuple[dict[Any, Any], list[Any], dict[Any, Any], dict[Any, Any], dict[Any, Any], str, str, Path, Path, dict[Any, Any], str, str, dict[Any, Any]]:
    """
        Summary:
            Load the data from the config file into the script variables and dictionaries

        Returns:
            tuple[dict[Any, Any], list[Any], dict[Any, Any], dict[Any, Any], \
            dict[Any, Any], str, str, Path, Path, \
            dict[Any, Any], str, str, dict[Any, Any]]: \
            All the variables and dictionaries loaded from the config.json file in a tuple
    """

    global main_paths, all_extensions, paths_dict, sub_paths, extensions_by_category, \
        exceptions, os_name, user_name, full_path, target_path, main_paths_str, \
        full_path_str, target_path_str

    os_name = config['OS']
    user_name = config['User']
    target_path = config['TargetPath']
    full_path = config['FullPath']
    paths_dict = config['Paths']

    full_path_str = str(Path(full_path))
    target_path_str = str(Path(target_path))

    # Diccionario de paths principales
    main_paths = {}
    for category, info in config['Paths'].items():
        main_paths[category] = info['Path']

    # Lista de todas las extensiones de todas las categorías
    all_extensions = []
    for category, info in config['Paths'].items():
        all_extensions.extend(info['Extensions'])

    # Diccionario de subruta
    sub_paths = {}
    for category, info in config['Paths'].items():
        for ext, path in info['Subrutas'].items():
            sub_paths[f"{category} - {ext}"] = path

    # Diccionario de extensiones por categoría
    extensions_by_category = {}
    for category, info in config['Paths'].items():
        extensions_by_category[category] = info['Extensions']

    # Diccionario de Excepciones
    exceptions = config['Excepciones']

    # Diccionario de paths principales en string
    main_paths_str = {}
    for category, path in main_paths.items():
        main_paths_str[category] = str(Path(path))

    return main_paths, all_extensions, sub_paths, extensions_by_category, \
        exceptions, os_name, user_name, full_path, target_path, main_paths_str, \
        full_path_str, target_path_str, paths_dict


def load_everything() -> Dict:
    """
        Summary 
            Load everything from the config file step by step calling the functions (load_config, load_data_from_config)
        Returns:
            Dict: Returns the configuration file loaded and the data from the config file loaded
    """
    config = load_config()
    try:
        load_data_from_config()
    except EnvironmentError as e:
        rprint(f"{ARROW} {ERROR} {e}")
        rprint(f"{ARROW} {
            ERROR} al cargar los datos de la configuración, \
            [bold yellow]por favor verifica que el json este bien formado[/bold yellow]")
        exit()
    return config


# *Utils Needed Functions for the script


def update_config(config: Dict) -> None:
    """
        Summary:
            Update the configuration file with the new data from the script \
            into the config.json file

        Args:
            config (Dict): The configuration file to update
    """
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)


def update_user_and_target_path(full_path: Path, config: Dict) -> None:
    """
        Summary:
            Update the user and target path in the config file base on the full path input into the config.json file

        Args:
            full_path (Path): The full path input
            config (Dict): The configuration file to update
    """
    if os.name == "posix":
        user_name = full_path.parts[-1]
        target_path = full_path.parts[-1]
    else:
        user_name = full_path.parts[-2]
        target_path = full_path.parts[-1]

    config['User'] = user_name
    config['TargetPath'] = target_path


# * Extra functions ( Not used in the script at the moment ) - Future implementation

def change_theme(variant: int) -> None:
    """
        Summary:
            The idea is to change the theme of the script base on the variant selected by the user

        Args:
            Variant (1) : Change the theme to green
            Variant (2) : Change the theme to red

        Future Implementation :
            More themes to be added 
    """

    if variant == 1:
        LINE_L.replace("blue", "green")
        LINE_R.replace("blue", "green")

    if variant == 2:
        LINE_L.replace("blue", "red")
        LINE_R.replace("blue", "red")


def clean_name(name) -> str:
    """
        Summary:
            Clean the name of the file or folder to avoid any special characters or spaces using regex

        Args:
            name (str): The name of the file or folder to clean

        Returns:
            str: Returns the name cleaned
    """

    clean_regex = re.compile(r"[^a-zA-Z0-9]")
    return clean_regex.sub("", name)


# * User Experience Functions

def clear_screen() -> None:
    """
        Summary:
            Clear the screen base on the OS (Windows or Linux) to give a better user experience 

    """
    # Validar el sistema operativo
    if os.name == 'posix':  # Linux
        os.system('clear')
    else:
        os.system('cls')  # Windows


# * Display Info

def user_info(variant: int) -> str | None:
    """
        Summary:
            Display the user info

        Args:
            variant 1 [int]: Display the user info in a table and return to the main menu
            variant 2 [int]: Display the user info in a table but don't return to the main menu

        Returns:
            str : Returns the prompt to the main menu
            None : Show the user info in a table but don't return to the main menu prompt
    """
    message = f"\n{ARROW_LINE_LEFT}Target Info{ARROW_LINE_RIGHT}\n"
    load_everything()
    check_config = Table("Configuración", "Valor")
    check_config.add_row("OS", os_name)
    check_config.add_row("User", user_name)
    check_config.add_row("TargetPath", target_path_str)
    check_config.add_row("FullPath", full_path_str)

    if variant == 1:
        rprint(message)
        rprint(check_config)
        main_menu()
        return __prompt_main__()

    if variant == 2:
        rprint(message)
        rprint(check_config)

    return None


def path_info(variant: int) -> str | None:
    """ 
        Summary:
            Display the path info base on the variant

        Args:
            variant 1: Display the paths in a table and return to the main menu
            variant 2: Display the paths in a table but don't return to the main menu

        Returns:
            str : Returns the prompt to the main menu
            None : Show the paths in a table but don't return to the main menu prompt
    """
    message = f"\n{ARROW_LINE_LEFT}Rutas{ARROW_LINE_RIGHT}\n"
    load_everything()
    check_rutas = Table("Número", "Carpeta", "Path")
    for i, (folder, path) in enumerate(main_paths.items(), start=1):
        check_rutas.add_row(str(i), folder, str(Path(path)))

    if variant == 1:
        rprint(message)
        rprint(check_rutas)
        main_menu()
        return __prompt_main__()

    if variant == 2:
        rprint(message)
        rprint(check_rutas)

    return None


def exceptions_info(variant: int) -> str | None:
    """ 
        Summary: 
            Display the exception info base on the variant

        Args:
            variant 1: Display the exceptions in a table and return to the main menu
            variant 2: Display the exceptions in a table but don't return to the main menu

        Returns:
            str : Returns the prompt to the main menu
            None : Show the exceptions in a table but don't return to the main menu prompt
    """
    message = f"\n{ARROW_LINE_LEFT}Excepciones{ARROW_LINE_RIGHT}\n"
    load_everything()
    check_excepciones = Table("Número", "Carpeta", "Path")
    for i, (excepcion, path_ex) in enumerate(config["Excepciones"].items(), start=1):
        check_excepciones.add_row(str(i), excepcion, str(Path(path_ex)))

    if variant == 1:
        rprint(message)
        rprint(check_excepciones)
        main_menu()
        return __prompt_main__()

    if variant == 2:
        rprint(message)
        rprint(check_excepciones)

    return None


def extensions_info(variant: int) -> str | None:
    """ 
        Summary:
            Display the extensions info base on the variant

        Args:
            variant 1: Display the extensions in a table and return to the main menu
            variant 2: Display the extensions in a table but don't return to the main menu

        Returns:
            str : Returns the prompt to the main menu
            None : Show the extensions in a table but don't return to the main menu prompt
    """
    message = f"\n{ARROW_LINE_LEFT}Extensiones{ARROW_LINE_RIGHT}\n"
    load_everything()
    check_extensiones = Table("Categoría", "Extensión")
    for category, extensions in extensions_by_category.items():
        extensions_str = '`,'.join([f"`{ext}`" for ext in extensions])
        check_extensiones.add_row(category, extensions_str)

    if variant == 1:
        rprint(message)
        rprint(check_extensiones)
        main_menu()
        return __prompt_main__()

    if variant == 2:
        rprint(message)
        rprint(check_extensiones)

    return None


def sub_paths_info(variant: int) -> str | None:
    """ 
        Summary:
            Display the sub paths info base on the variant

        Args:
            variant 1: Display the sub paths in a table and return to the main menu
            variant 2: Display the sub paths in a table but don't return to the main menu

        Returns:
            str : Returns the prompt to the main menu
            None : Show the sub paths in a table but don't return to the main menu prompt
    """
    message = f"\n{ARROW_LINE_LEFT}Subrutas{ARROW_LINE_RIGHT}\n"
    load_everything()
    for category, info in config['Paths'].items():
        check_sub_rutas = Table("Categoría", "Extensión", "Path")
        for ext, path in info['Subrutas'].items():
            check_sub_rutas.add_row(category, ext, path)
        rprint(message)
        rprint(check_sub_rutas)

    if variant == 1:
        rprint(message)
        rprint(check_sub_rutas)
        main_menu()
        return __prompt_main__()

    if variant == 2:
        rprint(message)
        rprint(check_sub_rutas)

    return None


def check() -> None:
    """
        Summary:
            Check all the info in the script and display it in a tables one by one to the user
    """
    user_info(2)
    path_info(2)
    exceptions_info(2)
    extensions_info(2)
    sub_paths_info(1)
    # ignore_file_info(2) - Future Implementation


# * Manejo del script , las Rutas y extensiones a través de la CLI con los menús


def main_menu() -> str:
    """
        Summary:
            Main menu to display the options to the user and handle the input

        Returns:
            str : Returns the prompt to the main menu
    """
    while True:
        rprint(f"\n{
            ARROW_LINE_LEFT}[bold purple]Menú Principal[/bold purple]{ARROW_LINE_RIGHT}\n")
        main_menu_table = Table("Comando", f'{DESCRIPTION_TEXT}')
        main_menu_table.add_row("0", "Setup inicial")
        main_menu_table.add_row("1", "Manejar Rutas")
        main_menu_table.add_row("2", "Manejar extensiones")
        main_menu_table.add_row("3", "Tabla de Rutas y extensiones")
        main_menu_table.add_row("4", "Ejecutar script")  # ?  Scripts
        main_menu_table.add_row("5", "Ver toda la configuración")
        main_menu_table.add_row("6", f"{SALIR}")
        rprint(main_menu_table)

        _ = __prompt_main__()


def root_folder():
    """
        Summary:
            Define where the files will be organized and update the config file with the new path selected by the user

        Returns:
            str : Returns the prompt to the main menu
    """
    rprint(f"{ARROW_LINE_LEFT}Target Folder{ARROW_LINE_RIGHT}\n")
    config = load_config()
    full_path = Path(config['FullPath'])
    update_user_and_target_path(full_path, config)
    root_folder_table = Table("Path")
    root_folder_table.add_row(target_path_str)
    config = load_config()
    rprint(root_folder_table)
    rprint(f"\n{ARROW} La carpeta Objetivo actual es: [bold purple]{
        config['FullPath']}[/bold purple]")
    change = typer.confirm(f"{ARROW} Desea cambiarla?")

    if change:
        rprint(f"{ARROW} Seleccione la nueva carpeta desde el explorador de archivos")
        full_path_input = filedialog.askdirectory()
        clear_screen()
        config['FullPath'] = full_path_input
        full_path_input = Path(full_path_input)

        update_user_and_target_path(full_path_input, config)
        update_paths_base_on_full_path(full_path_input, config)
        update_config(config)

        rprint(f"\n{ARROW} Carpeta FullPath actualizada exitosamente.\n")
        config = load_config()
        load_data_from_config()
        user_info(1)
        clear_screen()
        main_menu()
        return __prompt_main__()

    else:
        clear_screen()
        main_menu()
        return __prompt_main__()


def setup_menu() -> str:
    """
        Summary:
            Setup Menu to display the setup options to the user  

        Returns:
            str : Returns the prompt to the main menu to handle the input        
    """
    while True:
        rprint(f"\n{ARROW_LINE_LEFT}Setup{ARROW_LINE_RIGHT}\n")
        setup_menu_table = Table("Comando", f"{DESCRIPTION_TEXT}")
        setup_menu_table.add_row("1", "Definir la carpeta objetivo")
        setup_menu_table.add_row("2", f"{REGRESAR_MENU}")
        setup_menu_table.add_row("3", f"{SALIR}")
        rprint(setup_menu_table)

        _ = __prompt_setup_menu__()


def paths() -> str:
    """
        Summary:
            Paths Menu to display the paths options to the user

        Returns:
            str : Returns the prompt to the main menu to handle the input
    """
    while True:
        rprint(f"\n{ARROW_LINE_LEFT}Manejar Rutas{ARROW_LINE_RIGHT} \n")
        paths_menu_table = Table("Comando", f"{DESCRIPTION_TEXT}")
        paths_menu_table.add_row("1", "[bold green]Agregar ruta[/bold green]")
        paths_menu_table.add_row("2", "[bold red]Eliminar ruta[/bold red]")
        paths_menu_table.add_row("3", f"{REGRESAR_MENU}")
        paths_menu_table.add_row("4", f"{SALIR}")
        rprint(paths_menu_table)

        _ = __prompt_paths_menu__()


def extensions() -> str:
    """ 
        Summary:
            Extensions Menu to display the extensions options to the user

        Returns:
            str : Returns the prompt to the main menu to handle the input
    """
    while True:
        rprint(f"\n{ARROW_LINE_LEFT}Manejar extensiones{ARROW_LINE_RIGHT}\n")
        extensions_menu = Table("Comando", f"{DESCRIPTION_TEXT}")
        extensions_menu.add_row("0", "Ver todas las extensiones")
        extensions_menu.add_row(
            "1", "[bold green]Agregar extensión[/bold green]")
        extensions_menu.add_row("2", "[bold red]Eliminar extensión[/bold red]")
        extensions_menu.add_row("3", f"{REGRESAR_MENU}")
        extensions_menu.add_row("4", f"{SALIR}")
        rprint(extensions_menu)

        _ = __prompt_extensions_menu__()


def add_path_menu() -> str:
    """
        Summary:
            Add Path Menu to display the options to the user to add a path

        Returns:
            str : Returns the prompt to the main menu to handle the input
    """
    while True:
        rprint(f"\n{ARROW_LINE_LEFT}Ingrese si desea agregar una ruta de excepción o una ruta de organización{
            ARROW_LINE_RIGHT}\n")
        add_path_menu_table = Table("Comando", f"{DESCRIPTION_TEXT}")
        add_path_menu_table.add_row(
            "1", "[bold green]Ruta de excepción[/bold green]")
        add_path_menu_table.add_row(
            "2", "[bold blue]Ruta de organización[/bold blue]")
        add_path_menu_table.add_row(
            "3", "[bold red]Volver al menu anterior[/bold red]")
        add_path_menu_table.add_row("4", f"{REGRESAR_MENU}")
        add_path_menu_table.add_row("5", f"{SALIR}")
        rprint(add_path_menu_table)

        _ = __prompt_add_path_menu__()


def del_path_menu() -> str:
    """
        Summary:
            Delete Path Menu to display the options to the user to delete a path

        Returns:
            str : Returns the prompt to the main menu to handle the input
    """
    while True:
        rprint(f"\n{ARROW_LINE_LEFT}Ingrese si desea eliminar una ruta de excepción o una ruta de organización{
            ARROW_LINE_RIGHT}\n")
        del_path_menu_table = Table("Comando", f"{DESCRIPTION_TEXT}")
        del_path_menu_table.add_row(
            "1", "[bold green]Ruta de excepción[/bold green]")
        del_path_menu_table.add_row(
            "2", "[bold blue]Ruta de organización[/bold blue]")
        del_path_menu_table.add_row(
            "3", "[bold red]Volver al menu anterior[/bold red]")
        del_path_menu_table.add_row("4", f"{REGRESAR_MENU}")
        del_path_menu_table.add_row("5", f"{SALIR}")
        rprint(del_path_menu_table)

        _ = __prompt_del_path_menu__()


# * Manejo de preferencias


def add_exception_path() -> str:
    """
        Summary:
            Add an exception path to the config file

        Returns:
            str : Returns the prompt to the main menu to handle the input
    """
    rprint(f"\n{
           ARROW_LINE_LEFT}[bold green]Agregar Ruta de Excepción[/bold green]{ARROW_LINE_RIGHT}")
    rprint("[bold blue_violet]   Una ruta de excepción evita que los archivos de esa carpeta se muevan  [/bold blue_violet]")
    config = load_config()
    exceptions_info(2)

    # Seleccionar la carpeta de excepción
    rprint(f"{ARROW} Seleccione la nueva carpeta desde el explorador de archivos")
    path_except = filedialog.askdirectory()

    if not path_except:
        clear_screen()
        rprint(
            f"{ARROW} [bold yellow]No se ha seleccionado ninguna ruta[/bold yellow]")
        add_path_menu()
        return __prompt_add_path_menu__()

    exception_name = os.path.basename(path_except)

    # Verificar si la ruta de excepción ya existe
    if path_except in config["Excepciones"].values():
        clear_screen()
        rprint(f"{ARROW} La ruta [bold yellow]'{
               path_except}'[/bold yellow] ya existe.")
        confirmar = typer.confirm(
            f"{ARROW} ¿Desea actualizar la ruta de excepción?")

        # Actualizar la ruta de excepción
        if confirmar:
            if exception_name in config["Excepciones"]:
                rprint(f"{ARROW} El nombre de excepción [bold yellow]'{
                       exception_name}'[/bold yellow] ya existe.")
                exception_name = typer.prompt(
                    f"{ARROW} Ingrese un nuevo nombre para la excepción:")

            # Actualizar el nombre de la excepción
            config["Excepciones"][exception_name] = path_except
            update_config(config)
            clear_screen()
            rprint(f"{ARROW}Ruta de excepción [bold yellow]'{
                   exception_name}'[/bold yellow] [bold green]actualizada.[/bold green]")
            exceptions_info(1)
        else:
            clear_screen()
            rprint(f"{ARROW}{CANCELED_OPERATION}")
            add_path_menu()
            return __prompt_add_path_menu__()
    else:
        config["Excepciones"][exception_name] = path_except
        update_config(config)
        clear_screen()
        rprint(f"{ARROW}Ruta de excepción [bold yellow]'{
               exception_name}'[/bold yellow] [bold green]agregada.[/bold green]")
        exceptions_info(1)

    clear_screen()
    add_path_menu()
    return __prompt_add_path_menu__()


def remove_exception_path() -> str:
    """
        Summary:
            Remove an exception path from the config file

        Returns:
            str : Returns the prompt to the main menu to handle the input
    """
    rprint(f"\n{
           ARROW_LINE_LEFT}[bold red]Eliminar Ruta de Excepción[/bold red]{ARROW_LINE_RIGHT}")
    rprint("[bold blue_violet] Eliminar una ruta de excepción permitirá que los archivos de esa carpeta se muevan [/bold blue_violet]")

    config = load_config()
    exceptions_info(2)

    exception_names = list(config["Excepciones"].keys())
    if not exception_names:
        rprint(
            f"{ARROW} [bold red]No hay rutas de excepción para eliminar.[/bold red]")
        return __prompt_del_path_menu__()

    option = typer.prompt(
        f"{ARROW} Ingrese el número de la ruta de excepción a eliminar")

    try:
        option = int(option)
        if option < 1 or option > len(exception_names):
            raise ValueError
    except ValueError:
        clear_screen()
        rprint(
            f"{ARROW} [bold red]Opción inválida. Operación cancelada.[/bold red]")
        return __prompt_del_path_menu__()

    exception_name = exception_names[option - 1]

    # Confirmar eliminación
    confirm = typer.confirm(
        f"{ARROW} ¿Está seguro que desea eliminar la ruta de excepción '{exception_name}'?")

    if confirm:
        path_except = config["Excepciones"].pop(exception_name)
        update_config(config)
        clear_screen()
        rprint(f"{ARROW} Ruta de excepción [bold yellow]'{
               exception_name}'[/bold yellow] [bold green]eliminada.[/bold green]")
        exceptions_info(1)
    else:
        clear_screen()
        rprint(f"{ARROW} Eliminación de ruta de excepción [bold yellow]'{
               exception_name}'[/bold yellow] [bold red]cancelada.[/bold red]")

    add_path_menu()
    return __prompt_del_path_menu__()


def add_path() -> str:
    """
        Summary:
            Add a path to the config file

        Returns:
            str : Returns the prompt to the main menu to handle the input
    """
    rprint(
        f"\n{ARROW_LINE_LEFT}[bold green]Agregar Ruta[/bold green]{ARROW_LINE_RIGHT}")
    config = load_config()
    path_info(2)
    category = typer.prompt(
        f"{ARROW} Ingrese la categoría de la ruta que desea agregar (e.g., Fotos, Videos): ")
    path = filedialog.askdirectory()
    path = os.path.join(path, category)
    if path == "":
        clear_screen()
        rprint(
            f"{ARROW} [bold yellow]No se ha seleccionado ninguna ruta[/bold yellow]")
        return __prompt_add_path_menu__()
    if category in config["Excepciones"].values():
        clear_screen()
        rprint(f"{ARROW} La ruta [bold yellow]'{
               category}'[/bold yellow] ya es una excepción.")
        return __prompt_add_path_menu__()

    if path in config["Paths"]:
        rprint(f"{ARROW} La categoría [bold purple]'{
               category}'[/bold purple] ya existe.")
        return __prompt_paths_menu__()
    else:
        config["Paths"][category] = {
            "Path": path, "Extensions": [], "Subrutas": {}}
        update_config(config)
        clear_screen()
        rprint(f"{ARROW}Ruta de la categoría [bold purple]'{
               category}'[/bold purple] [bold green]agregada.[/bold green]")
        paths()
        return __prompt_add_path_menu__()


def remove_path() -> str:
    """
        Summary:
            Remove a path from the config file and all the subpaths associated with it

        Returns:
            str : Returns the prompt to the del path menu menu to handle the input
    """
    rprint(
        f"\n{ARROW_LINE_LEFT}[bold red]Eliminar Ruta[/bold red]{ARROW_LINE_RIGHT}")
    rprint(
        f"{ARROW}[bold yellow] Esto eliminará la ruta y todas las subrutas asociadas a ella.[/bold yellow]")
    config = load_config()
    path_info(2)

    # Obtener las rutas y sus categorías
    categories = list(config["Paths"].keys())
    if not categories:
        rprint(f"{ARROW} [bold red]No hay rutas para eliminar.[/bold red]")
        return __prompt_paths_menu__()

    option = typer.prompt(f"{ARROW} Ingrese el número de la ruta a eliminar")

    try:
        option = int(option)
        if option < 1 or option > len(categories):
            raise ValueError
    except ValueError:
        clear_screen()
        rprint(
            f"{ARROW} [bold red]Opción inválida. Operación cancelada.[/bold red]")
        return __prompt_paths_menu__()

    category = categories[option - 1]

    confirmar = typer.confirm(
        f"{ARROW} ¿Está seguro de que desea eliminar la categoría '{category}' y todas su rutas? : ")
    if not confirmar:
        clear_screen()
        rprint(f"{ARROW_LINE_LEFT}{CANCELED_OPERATION}{ARROW_LINE_RIGHT}")
        paths()
        return __prompt_paths_menu__()

    del config["Paths"][category]
    update_config(config)
    clear_screen()
    rprint(f"{ARROW} Rutas de la categoría [bold purple]'{
           category}'[/bold purple] [bold orange_red1]eliminadas.[/bold orange_red1]")

    paths()
    return __prompt_paths_menu__()


def add_extension():
    """_summary_ Add an extension to the config file
    """
    rprint(f"\n{
           ARROW_LINE_LEFT}[bold green]Agregar Extensión[/bold green]{ARROW_LINE_RIGHT}\n")
    config = load_config()
    extensions_info(2)
    category = input(
        f"{ARROW}Ingrese la categoría (e.g., Documentos, Musica: ")
    extension = input(
        f"{ARROW}Ingrese la extensión a agregar (e.g., MP4, JPG): ").upper()
    if category in config["Paths"]:
        if extension not in config["Paths"][category]["Extensions"]:
            config["Paths"][category]["Extensions"].append(extension)
            # Crear la subruta para la extensión
            subruta = os.path.join(
                config["Paths"][category]["Path"], extension)
            config["Paths"][category]["Subrutas"][extension] = subruta
            update_config(config)
            clear_screen()
            rprint(f"{ARROW}Extensión '{
                   extension}' agregada a la categoría '{category}'.")
            main_menu()
            return __prompt_main__()

        else:
            clear_screen()
            rprint(f"{ARROW}La extensión '{
                   extension}' ya existe en la categoría '{category}'.")
            extensions()
            return __prompt_extensions_menu__()

    else:
        clear_screen()
        rprint(f"{ARROW}La categoría '{category}' no existe.")
        extensions()
        return __prompt_extensions_menu__()


def remove_extension():
    """_summary_ Remove an extension from the config file
    """
    rprint(
        f"\n{ARROW_LINE_LEFT}[bold red]Eliminar Extensión[/bold red]{ARROW_LINE_RIGHT}\n")
    config = load_config()
    extensions_info(2)
    category = input(
        f"{ARROW}Ingrese la categoría de la extensión a eliminar (e.g. Videos, Documentos): ")
    extension = input(
        f"{ARROW}Ingrese la extensión a eliminar (e.g. MP4, JPG): ").upper()
    if category in config["Paths"]:
        if extension in config["Paths"][category]["Extensions"]:
            confirmar = typer.confirm(
                f"{ARROW}¿Está seguro de que desea eliminar la extensión '{extension}' de la categoría '{category}'? : ")
            if not confirmar:
                clear_screen()
                rprint(
                    f"{ARROW_LINE_LEFT}{CANCELED_OPERATION}{ARROW_LINE_RIGHT}")
                extensions()
                return __prompt_extensions_menu__()

            if confirmar:
                config["Paths"][category]["Extensions"].remove(extension)
                del config["Paths"][category]["Subrutas"][extension]
                update_config(config)
                clear_screen()
                rprint(
                    f"{ARROW}Extensión '{extension}' eliminada de la categoría '{category}'.")
                extensions()
                return __prompt_extensions_menu__()

        else:
            clear_screen()
            rprint(f"La extensión [bold blue_violet]'{
                   extension}'[/bold blue_violet] no existe en la categoría '{category}'.")
            extensions()
            return __prompt_extensions_menu__()


def update_paths_base_on_full_path(full_path_input, config: Dict) -> None:
    """
        Summary:
            Update the paths base on the full path input by the user

        Args:
            full_path_input (Path): The full path input by the user
            config (Dict): The configuration file to update
    """
    full_path_input = str(full_path_input)
    for category, details in config["Paths"].items():
        # Actualizar la ruta de la categoría
        details["Path"] = os.path.join(full_path_input, category)
        rprint(f"{ARROW} Nueva ruta para la categoría [bold yellow]{
               category}[/bold yellow] : [bold green]{details['Path']}[/bold green]")

        # Actualizar las subrutas dentro de la ruta de la categoría
        for ext in details["Subrutas"]:
            details["Subrutas"][ext] = os.path.join(details["Path"], ext)
            rprint(f"{ARROW} Nueva subruta para la categoría [bold purple]{
                   category}[/bold purple] y extensión [bold blue]{ext}[/bold blue] : [bold green]{details['Subrutas'][ext]}[/bold green]")

    update_config(config)


# * Manejo del input de la CLI


def __prompt_main__() -> str:
    """
        Summary:
            Main menu management
            Handle the main menu using typer

        Returns:
            str : Returns the prompt to the main menu
    """
    prompt = typer.prompt(f"{ARROWLINE}")
    load_everything()
    match prompt:
        case "0":
            clear_screen()
            setup_menu()
            return __prompt_main__()

        case "1":
            clear_screen()
            paths()
            return __prompt_main__()

        case "2":
            clear_screen()
            extensions()
            return __prompt_main__()

        case "3":
            clear_screen()
            path_info(2)
            extensions_info(1)
            return __prompt_main__()

        case "4":
            clear_screen()
            main()
            return __prompt_main__()

        case "5":
            clear_screen()
            check()
            return __prompt_main__()

        case "6":
            clear_screen()
            typer.echo(EXIT)
            raise typer.Abort()

        case _:
            typer.echo(DEFAULT_ERROR)
            return __prompt_main__()


def __prompt_setup_menu__() -> str:
    """
        Summary:
            Setup menu management
            Handle the setup menu using typer

        Returns:
            str : Returns the prompt to the main menu
    """
    prompt = typer.prompt(f"{ARROWLINE}")
    match prompt:
        case "1":
            clear_screen()
            root_folder()
            return __prompt_setup_menu__()

        case "2":
            clear_screen()
            main_menu()
            return __prompt_main__()

        case "3":
            clear_screen()
            typer.echo(EXIT)
            raise typer.Abort()

        case _:
            typer.echo(DEFAULT_ERROR)
            return __prompt_setup_menu__()


def __prompt_paths_menu__() -> str:
    """
        Summary:
            Paths menu management
            Handle the paths menu using typer

        Returns:
            str : Returns the prompt to the main menu
    """
    prompt = typer.prompt(f"{ARROWLINE}")
    match prompt:
        case "1":
            clear_screen()
            add_path_menu()
            return __prompt_add_path_menu__()

        case "2":
            clear_screen()
            del_path_menu()
            return __prompt_del_path_menu__()

        case "3":
            clear_screen()
            main_menu()
            return __prompt_main__()

        case "4":
            clear_screen()
            typer.echo(EXIT)
            raise typer.Abort()

        case _:
            typer.echo(DEFAULT_ERROR)
            return __prompt_paths_menu__()


def __prompt_add_path_menu__() -> str:
    """
        Summary:
            Add path menu management
            Handle the add path menu using typer

        Returns:
            str : Returns the prompt to the main menu
    """
    prompt = typer.prompt(f"{ARROWLINE}")
    match prompt:
        case "1":
            clear_screen()
            add_exception_path()
            return __prompt_add_path_menu__()

        case "2":
            clear_screen()
            add_path()
            return __prompt_add_path_menu__()

        case "3":
            clear_screen()
            paths()
            return __prompt_paths_menu__()

        case "4":
            clear_screen()
            main_menu()
            return __prompt_main__()

        case "5":
            clear_screen()
            typer.echo(EXIT)
            raise typer.Abort()

        case _:
            typer.echo(DEFAULT_ERROR)
            return __prompt_add_path_menu__()


def __prompt_del_path_menu__() -> str:
    """
        Summary:
            Delete path menu management
            Handle the delete path menu using typer

        Returns:
            str : Returns the prompt to the main menu
    """
    prompt = typer.prompt(f"{ARROWLINE}")
    match prompt:
        case "1":
            clear_screen()
            remove_exception_path()
            return __prompt_del_path_menu__()

        case "2":
            clear_screen()
            remove_path()
            return __prompt_del_path_menu__()

        case "3":
            clear_screen()
            paths()
            return __prompt_paths_menu__()

        case "4":
            clear_screen()
            main_menu()
            return __prompt_main__()

        case "5":
            clear_screen()
            typer.echo(EXIT)
            raise typer.Abort()

        case _:
            typer.echo(DEFAULT_ERROR)
            return __prompt_del_path_menu__()


def __prompt_extensions_menu__() -> str:
    """
        Summary:
            Extensions menu management
            Handle the extensions menu using typer

        Returns:
            str : Returns the prompt to the main menu
    """
    prompt = typer.prompt(f"{ARROWLINE}")
    match prompt:
        case "0":
            extensions_info(1)
            return __prompt_extensions_menu__()

        case "1":
            clear_screen()
            add_extension()
            return __prompt_extensions_menu__()

        case "2":
            clear_screen()
            remove_extension()
            return __prompt_extensions_menu__()

        case "3":
            clear_screen()
            main_menu()
            return __prompt_main__()

        case "4":
            clear_screen()
            typer.echo(EXIT)
            raise typer.Abort()

        case _:
            typer.echo(DEFAULT_ERROR)
            return __prompt_extensions_menu__()


# * Script principal (Organizador de archivos)


def is_exception(path, exceptions) -> bool:
    """
        Summary:
            Check if the path is an exception of is inside an exception folder

        Args:
            path (str): The path to check
            exceptions (Dict[str, str]): The exceptions to check

        Returns:
            bool: Returns True if the path is an exception, False otherwise
    """
    # Normaliza la ruta a comprobar
    path = os.path.abspath(os.path.normpath(path))

    for exc in exceptions.values():
        # Normaliza cada excepción
        exc = os.path.abspath(os.path.normpath(exc))
        # Verifica si el path comienza con la excepción
        if path.startswith(exc):
            # ? Testing  rprint(f"{ARROW} La ruta [bold yellow]'{path}'[/bold yellow] es una excepción")
            return True
    return False


def explorar_directorios(full_path: Path, exceptions: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """
        Summary:
            Explore the directories and files to organize and check \
            if they are exceptions or inside an exception folder

        Args:
            full_path (Path): La ruta base desde donde empezar a explorar.
            exceptions (Dict[str, str]): Un diccionario con las excepciones \
                que se le pasan a is_exception.

        Returns:
            Tuple[List[str], List[str]]: Una tupla con dos listas, \
            la primera con rutas de archivos a organizar \
            y la segunda con rutas de archivos y directorios \
            dentro de excepciones.
    """
    # Lista de archivos a organizar
    global archivos_a_organizar, archivos_dentro_de_excepciones, carpetas_revisadas
    archivos_a_organizar = []
    carpetas_revisadas = []
    archivos_dentro_de_excepciones = []

    for root, _, files in os.walk(full_path):
        rprint(f"{ARROW} Explorando [bold green]{root}[/bold green]...")
        if not is_exception(root, exceptions):
            carpetas_revisadas.append(root)
            for file in files:
                archivo_completo = os.path.join(root, file)
                if not is_exception(archivo_completo, exceptions):
                    archivos_a_organizar.append(archivo_completo)
                    rprint(f"{ARROW} Archivo [bold yellow]{
                           file}[/bold yellow] agregado a la lista de archivos a organizar")
                else:
                    archivos_dentro_de_excepciones.append(archivo_completo)
                    rprint(f"{ARROW} Archivo [bold red]{
                           file}[/bold red] está dentro de excepciones")
        else:
            archivos_dentro_de_excepciones.append(root)
            rprint(f"{ARROW} Directorio [bold red]{
                   root}[/bold red] está dentro de excepciones")

    return archivos_a_organizar, archivos_dentro_de_excepciones


def mover_archivos(archivos_a_organizar: List[str],  paths_dict: Dict) -> None:
    """
        Summary:
            Mueve los archivos a organizar a sus respectivas carpetas.

        Args:
            archivos_a_organizar (List[str]): Una lista de rutas de archivos a organizar.
            config (Dict): La configuración del script.
    """

    for archivo in archivos_a_organizar:
        extension = archivo.split('.')[-1].upper()
        archivo_path = Path(archivo).resolve()
        archivo_movido = False  # Bandera para verificar si el archivo ha sido movido

        for _, detalles in paths_dict.items():
            if extension in detalles["Extensions"]:
                _ = Path(detalles["Path"]).resolve()
                destino_subcarpeta = Path(detalles["Subrutas"].get(
                    extension, detalles["Path"])).resolve()
                destino_final = destino_subcarpeta / archivo_path.name

                # Verificar si la ruta actual y la de destino son iguales
                if archivo_path == destino_final:
                    rprint(f"{ARROW} Archivo [bold yellow]{
                           archivo}[/bold yellow] ya está en [bold green]{destino_final}[/bold green], no se mueve.")
                else:
                    # Crear subcarpeta si no existe
                    os.makedirs(destino_subcarpeta, exist_ok=True)
                    # Mover el archivo a la subcarpeta correspondiente
                    shutil.move(archivo, destino_final)
                    rprint(f"{ARROW} Archivo [bold yellow]{
                           archivo}[/bold yellow] movido a [bold green]{destino_final}[/bold green]")
                archivo_movido = True
                break

        if not archivo_movido:
            rprint(f"{ARROW} No se encontró una categoría para el archivo [bold yellow]{
                   archivo}[/bold yellow] con extensión [bold red]{extension}[/bold red]")


def del_empty_folders(carpetas_revisadas: List[str]) -> None:
    """
        Summary:
            Elimina las carpetas vacías de una lista de carpetas.

        Args:
            carpetas (List[str]): Una lista de rutas de carpetas a verificar y eliminar si están vacías.
    """
    for carpeta in carpetas_revisadas:
        try:
            if not os.listdir(carpeta):
                os.rmdir(carpeta)
                rprint(f"{ARROW} Carpeta vacía [bold red]{
                       carpeta}[/bold red] eliminada.")
            else:
                rprint(f"{ARROW} Carpeta [bold green]{
                       carpeta}[/bold green] no está vacía.")
        except OSError as e:
            rprint(f"{ARROW} No se pudo eliminar la carpeta [bold red]{
                   carpeta}[/bold red]: {e}")


def run_main_script() -> str:
    """Run all the functions of the script"""
    try:
        rprint(f"{ARROW} Iniciando script...\n")
        time.sleep(2)
        load_everything()
        rprint(f"{ARROW} Folder de ejecución del script : [bold green]{
            full_path_str}[/bold green]...\n")
        time.sleep(1)
        rprint(
            f"{ARROW} Iniciando [bold hot_pink]Fase #1[/bold hot_pink] : Exploración de archivos...\n")
        time.sleep(2)
        explorar_directorios(full_path, exceptions)
        rprint(
            f"\n{ARROW} [bold hot_pink]Fase #1[/bold hot_pink] : Exploración de archivos completada\n")
        rprint(
            f"{ARROW} Iniciando [bold hot_pink]Fase #2[/bold hot_pink] : Organización de archivos...\n")
        time.sleep(2)
        mover_archivos(archivos_a_organizar, paths_dict)
        rprint(
            f"\n{ARROW} [bold hot_pink]Fase #2[/bold hot_pink] : Organización de archivos completada\n")
        time.sleep(2)
        clear_screen()
        rprint(
            f"{ARROW} Iniciando [bold hot_pink]Fase #3[/bold hot_pink] : Eliminación de carpetas vacías...\n")
        time.sleep(1)
        del_empty_folders(carpetas_revisadas)
        rprint(f"\n{ARROW} Script finalizado con éxito\n")
        time.sleep(1)
        rprint(f"{ARROW} Volviendo al menu principal...")
        time.sleep(2)
        clear_screen()
        main_menu()
        return __prompt_main__()

    except OSError as e:
        rprint(f"{ARROW} {e} al ejecutar el script")
        exit()


# * Entry Point


def main() -> None:
    """
        Summary:
            Entry point of the CLI App 

        Future Implementation:
            Add more script to run , so in the future the user can select \
            which script to run and instead of running 
            the main script it will run a function that controls \
            the script to run based on the user input
    """
    run_main_script()


if __name__ == "__main__":
    clear_screen()
    load_everything()
    typer.run(main_menu)
