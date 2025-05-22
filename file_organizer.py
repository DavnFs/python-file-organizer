import os
import shutil
import logging
from pathlib import Path
import time

# --- BASIC CONFIGURATION ---
# Replace with the path to the directory you want to organize (e.g., your Downloads folder)
# IMPORTANT: Be careful when testing; ensure you know what this script does.
# It's highly recommended to test first on a sample folder containing dummy files.
# Example for Windows: SOURCE_DIRECTORY = r"C:\Users\YourName\Downloads"
# Example for macOS/Linux: SOURCE_DIRECTORY = "/Users/YourName/Downloads"
SOURCE_DIRECTORY = r"D:\FOLDER_TO_ORGANIZE_TEST" # <--- CHANGE THIS TO YOUR TARGET DIRECTORY!

# Mapping of extensions to destination folder names (created within SOURCE_DIRECTORY)
# You can add more extensions and folders here
FOLDER_MAPPINGS = {
    # Documents
    ".pdf": "PDFs",
    ".docx": "Documents",
    ".doc": "Documents",
    ".txt": "TextFiles",
    ".pptx": "Presentations",
    ".xlsx": "Spreadsheets",
    ".csv": "CSVs",
    ".ipynb": "Notebooks",
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".svg": "Images",
    ".heic": "Images",
    # Audio
    ".mp3": "Music",
    ".wav": "Music",
    ".aac": "Music",
    ".flac": "Music",
    # Video
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".avi": "Videos",
    ".mov": "Videos",
    # Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".tar.gz": "Archives",
    ".7z": "Archives",
    # Applications/Installers
    ".exe": "Installers",
    ".msi": "Installers",
    # Other common types
    ".torrent": "Torrents",
    # Default folders
    "__OTHER__": "Others",       # For files with unmapped extensions
    "__NO_EXTENSION__": "NoExtension" # For files without any extension
}

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("file_organizer.log", mode='a'), # Log to file (append mode)
        logging.StreamHandler()                             # Log to console as well
    ]
)

def get_file_extension(file_path: Path) -> str:
    """Gets the file extension in lowercase."""
    # Path.suffix returns the extension with a dot (e.g., ".txt")
    # Special handling for double extensions like .tar.gz
    if file_path.name.endswith(".tar.gz"):
        return ".tar.gz"
    return file_path.suffix.lower()

def get_unique_destination_path(original_destination_path: Path) -> Path:
    """
    If the destination path already exists, this function generates a new unique path
    by appending a version number, e.g., file.txt -> file (1).txt.
    """
    if not original_destination_path.exists():
        return original_destination_path

    parent_dir = original_destination_path.parent
    file_stem = original_destination_path.stem # Filename part without extension
    file_suffix = original_destination_path.suffix # File extension (e.g., ".txt")

    count = 1
    # Loop to find a unique filename by appending (number)
    while True:
        new_file_name = f"{file_stem} ({count}){file_suffix}"
        new_destination_path = parent_dir / new_file_name
        if not new_destination_path.exists():
            logging.info(f"File '{original_destination_path.name}' already exists. Will be renamed to '{new_file_name}'.")
            return new_destination_path
        count += 1
        # Safety break if there are an excessive number of similarly named files
        if count > 100: # You can adjust this limit
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            fallback_new_name = f"{file_stem}_{timestamp}{file_suffix}"
            fallback_destination_path = parent_dir / fallback_new_name
            # Assume low probability of timestamp collision, but could be checked
            if not fallback_destination_path.exists():
                 logging.warning(f"Too many duplicate versions for '{original_destination_path.name}'. Renaming with timestamp to '{fallback_new_name}'.")
                 return fallback_destination_path
            else: # Extremely rare, but for robustness
                import uuid
                unique_id = str(uuid.uuid4())[:8]
                super_unique_name = f"{file_stem}_{timestamp}_{unique_id}{file_suffix}"
                logging.warning(f"Timestamp collision too! Renaming with UUID to '{super_unique_name}'.")
                return parent_dir / super_unique_name

def organize_files(source_dir_str: str, mappings: dict):
    """
    Organizes files in the source_dir based on extension mappings,
    with duplicate file handling (rename).
    """
    source_path = Path(source_dir_str)

    if not source_path.is_dir():
        logging.error(f"Source directory not found: {source_dir_str}")
        return

    logging.info(f"Starting file organization in: {source_path}")

    for item in source_path.iterdir(): # Iterate over all items (files and folders) in source_dir
        if item.is_file(): # Only process files, ignore subdirectories
            file_extension = get_file_extension(item)

            # Determine the target folder name
            if file_extension:
                target_folder_name = mappings.get(file_extension, mappings["__OTHER__"])
            else: # No extension
                target_folder_name = mappings["__NO_EXTENSION__"]

            target_dir_path = source_path / target_folder_name # Create full path to target folder

            # Create target folder if it doesn't exist
            try:
                target_dir_path.mkdir(parents=True, exist_ok=True)
                # parents=True: create parent directories if needed (e.g., Documents/PDFs)
                # exist_ok=True: don't raise error if folder already exists
            except OSError as e:
                logging.error(f"Could not create destination directory {target_dir_path}: {e}")
                continue # Skip to the next file if folder creation fails

            # Original intended destination path
            original_destination_file_path = target_dir_path / item.name

            # Get a unique destination path (renames if duplicate exists)
            final_destination_path = get_unique_destination_path(original_destination_file_path)

            # Move the file
            try:
                shutil.move(str(item), str(final_destination_path))
                log_message = f"Moved: {item.name}  --->  {target_folder_name}/{final_destination_path.name}"
                if final_destination_path.name != item.name:
                    log_message += " (renamed due to duplicate)"
                logging.info(log_message)
            except Exception as e:
                logging.error(f"Failed to move {item.name} to {final_destination_path}: {e}")
        else:
            logging.debug(f"Skipping directory: {item.name}")

    logging.info("File organization process completed.")

if __name__ == "__main__":
    # IMPORTANT: Review SOURCE_DIRECTORY and FOLDER_MAPPINGS before running!
    # Consider adding user confirmation before starting.

    confirm = input(f"You are about to organize files in '{SOURCE_DIRECTORY}'. Files with the same name will be renamed. Continue? (y/n): ")
    if confirm.lower() == 'y':
        organize_files(SOURCE_DIRECTORY, FOLDER_MAPPINGS)
    else:
        logging.info("Operation cancelled by user.")