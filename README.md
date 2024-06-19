# Yuu Tools - CLI APP to manage and run scripts

Yuu Tools is a CLI application that allows you to manage and run scripts in a simple and organized way using menus on the command line.

## Features

- Manage the config file from the CLI app
- Run scripts in a simple and organized way
- Focusing on the user experience on the command line
- Easy to use and configure
- Log system to track the execution of the scripts
- More Features coming soon

## Script -> Sort Files

## Features of the script

- Recursively explore a root folder and its subfolders to find files to organize.
- Move files to corresponding folders based on defined extensions and categories.
- Ignore files and folders marked as exceptions.
- Delete empty folders after organization.
- Easy configuration of paths, extensions, and exceptions through a JSON file managed by the CLI app.

## Script Roadmap

- Add more file/folder operations like copy, move, rename
- Support additional file attributes to organize (size, date etc)

## More scripts coming soon

## Installation

```bash
    git clone https://github.com/Yuzu02/Yuu-Tools.git
    cd organizador-de-archivos
    pip install -r requirements.txt
```

## Usage

```bash
    python yuu_tools.py
```

## Setup

- The first time you run the application, it will ask you to create a configuration file.
- The configuration file will be created in the same directory as the application.
- The configuration file will be named `config.json`.
- The configuration file will be used to store the info needed to run the scripts.
- The configuration file will have the a base structure to modify at your convenience by the CLI app.
- Now you can manage and run scripts from the CLI app.

## Contributing

This project is open to contributions, suggestions, and improvements. Feel free to contribute to this project by creating a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
