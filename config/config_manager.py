""" 
    Summary:
        Module to manage the configuration of the application using a json file
"""

import json
import os
from yuu_tools import CONFIG_FILE


class ConfigManager:
    """
        Summary:
            Class to manage the configuration of the application using a json file

        Attributes:
            config_file (str): Name of the configuration file
            config (dict): Dictionary with the configuration of the application

        Methods:
            load_config: Load the configuration from the file
            create_config: Create the default configuration
            save_config: Save the configuration to the file
            update_config: Update the configuration with a new value
    """

    def __init__(self, config_file="config.json"):
        """ 
            Summary:
                Constructor of the class ConfigManager

            Args:
                config_file (str): Name of the configuration file (default: "config.json")      
        """
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """
            Summary:
                Carga la configuración desde el archivo

            Returns:
                dict: Diccionario con la configuración de la aplicación
        """
        if not os.path.exists(self.config_file):
            return self.create_config()
        with open(self.config_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    def create_config(self):
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

    def save_config(self):
        """
            Summary:
                Save the configuration in the file config.json
        """
        with open(self.config_file, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, indent=4)

    def update_config(self, key, value):
        """
            Summary:
                Update the configuration with a new value

            Args:
                key (str): Key to update
                value (str): New value to update
        """
        self.config[key] = value
        self.save_config()
