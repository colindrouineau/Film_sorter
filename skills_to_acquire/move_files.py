import os
import shutil


def move_and_rename_file(source_path, destination_path):
    try:
        # Move and rename the file
        shutil.move(source_path, destination_path)
        print(
            f"File moved and renamed successfully from {source_path} to {destination_path}"
        )
    except FileNotFoundError:
        print(f"Error: The file {source_path} does not exist.")
    except PermissionError:
        print(f"Error: Permission denied when trying to move {source_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_folder(folder_path):
    try: # ALREADY EXISTED  os.path.isdir(directory_path): if os.path.isfile(file_path):
        # Create the directory
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created successfully at {folder_path}")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")


def delete_empty_folder(folder_path):
    try:
        # Remove the directory
        os.rmdir(folder_path)
        print(f"Empty folder deleted successfully at {folder_path}")
    except OSError as e:
        print(f"Error: {folder_path} : {e.strerror}")


# Example usage
source_path = "C:\\colin_films\\time_mastersiki.uwu"
destination_path = "C:\\colin_films\\TIME_MASTERS\\time_masters.mkv"  # Replace with your source file path
move_and_rename_file(source_path, destination_path)


'''

file_path = "C:\\colin_films\\TIME_MASTERS\\time_masters.mkv"
# Example usage
folder_path = "C:\\colin_films\\TIME_MASTERS_newhaha"  # Replace with your desired folder path
create_folder(folder_path)


# Example usage
folder_path = "C:\\colin_films\\TIME_MASTERS_newhaha"  # Replace with the path of the empty folder you want to delete
delete_empty_folder(folder_path)
'''