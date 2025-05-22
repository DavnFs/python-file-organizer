# Python File Organizer

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A simple yet effective Python script to help you tidy up messy directories by organizing files into subdirectories based on their file type (extension) and handling duplicate files gracefully.

## Description

This project provides a Python script that scans a specified source directory and moves files into appropriate subfolders based on a configurable extension mapping. If a file with the same name already exists in the destination folder, this script will automatically rename the new file to prevent data overwriting.

It's particularly useful for cleaning up your "Downloads" folder or any other directory that tends to accumulate various file types.

## Current Features

* **Extension-Based Organization:** Files are sorted into folders based on their extensions (e.g., `.pdf` files go to a "PDFs" folder, `.jpg` files to an "Images" folder).
* **Automatic Folder Creation:** If a target folder doesn't exist, the script creates it.
* **Duplicate File Handling:** If a file with the same name already exists in the destination directory, the new file is renamed by appending a version number (e.g., `filename (1).ext`, `filename (2).ext`, etc.) or a timestamp if too many versions exist.
* **Logging:** All move actions and any errors are logged to a `file_organizer.log` file and also printed to the console.
* **Easy Configuration:** Extension-to-folder mappings and the source directory are easily configured directly within the script.
* **Modern Path Handling:** Uses `pathlib` for robust and cross-platform file path management.

## Prerequisites

* Python 3.7 or higher.
* No external libraries are required beyond Python's standard library (`os`, `shutil`, `logging`, `pathlib`, `time`).

## How to Use

1.  **Clone or Download the Repository:**
    ```bash
    # If it's on GitHub:
    # git clone [https://github.com/DavnFs/python-file-organizer.git)
    # cd python-file-organizer
    ```
    Alternatively, just download/copy the `.py` script to your computer.

2.  **Configure the Script (e.g., `file_organizer.py`):**
    * Open the script file with a text editor.
    * **IMPORTANT:** Modify the `SOURCE_DIRECTORY` variable to the absolute path of the directory you want to organize.
        ```python
        SOURCE_DIRECTORY = r"C:\Users\YourName\FolderToOrganize"
        # or for macOS/Linux:
        # SOURCE_DIRECTORY = "/Users/YourName/FolderToOrganize"
        ```
        **WARNING:** It is strongly recommended to test this script on a sample directory with dummy files first before running it on important directories.
    * Adjust the `FOLDER_MAPPINGS` dictionary if you want to change the destination folders for specific extensions or add new ones.
        ```python
        FOLDER_MAPPINGS = {
            ".pdf": "PDF_Documents", // Folder names can be customized
            ".jpg": "My_Pictures",
            # ...and so on
        }
        ```

3.  **Run the Script:**
    Open your terminal or command prompt, navigate to the directory where you saved the script, and execute:
    ```bash
    python your_script_name.py
    ```
    For example:
    ```bash
    python file_organizer.py
    ```
    The script will ask for confirmation before starting the organization process.

4.  **Check the Results:**
    * Files in your `SOURCE_DIRECTORY` will be moved into their respective subdirectories.
    * A log file named `file_organizer.log` will be created/updated in the same directory as the script, containing details of the operations.

## Future Enhancements

* [ ] Read configuration from an external file (JSON/YAML).
* [ ] Add a "Dry Run" option to preview changes without actually moving files.
* [ ] Organize files by creation/modification date.
* [ ] Real-time directory monitoring (using a library like `watchdog`).
* [ ] A simple Graphical User Interface (GUI).

## License

This project is licensed under the [MIT License](LICENSE.txt).
