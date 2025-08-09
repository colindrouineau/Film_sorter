from pymediainfo import MediaInfo
from CONFIG import *
import os
import shutil
import utils as u
import db
from pathlib import Path
import requests
import base64


def convert_milliseconds(milliseconds):
    # Calculate total seconds
    total_seconds = milliseconds // 1000

    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds


# return duration as (hours, minutes, seconds), languages and subtitles as a list of the available ones.
def extract_video_metadata(file_path, test=False):
    media_info = MediaInfo.parse(file_path)
    duration = None
    languages = []
    subtitles = []

    for track in media_info.tracks:
        if track.track_type == "General":
            if track.duration == None:
                duration = "Unknown"
            else:
                duration = convert_milliseconds(int(float(track.duration)))
                duration = (
                    str(duration[0])
                    + " h "
                    + str(duration[1])
                    + " m "
                    + str(duration[2])
                    + " s "
                )
        elif track.track_type == "Audio":
            if track.other_language == None:
                languages.append("Piste " + str(len(languages) + 1))
            else:
                languages.append(track.other_language[0])
        elif track.track_type == "Text":
            if track.other_language == None:
                subtitles.append("Piste " + str(len(subtitles) + 1))
            else:
                subtitles.append(track.other_language[0])

    if test:
        print(f"Duration: {duration}")
        print(f"audio : {languages}")
        print(f"subtitles : {subtitles}")

    return duration, languages, subtitles


def text_formatter(text, test=False):
    punc_sep = u.punctuation_split(text)
    extension = punc_sep.pop()
    formatted_text = " ".join(punc_sep)
    formatted_text += "." + extension
    # First letter in capital
    formatted_text = formatted_text[0].upper() + formatted_text[1:].lower()
    if test:
        print(formatted_text)
    return formatted_text


def move_and_rename_file(source_path, destination_path, test=False):
    try:
        # Move and rename the file
        shutil.move(source_path, destination_path)
        if test:
            print(
                f"File moved and renamed successfully from {source_path} to {destination_path}"
            )
    except FileNotFoundError:
        print(f"Error: The file {source_path} does not exist.")
    except PermissionError:
        print(f"Error: Permission denied when trying to move {source_path}.")
    except FileExistsError:
        print(
            f"The destination path '{destination_path}' already exists. Handling the error..."
        )
        move_and_rename_file(source_path, Path(str(destination_path) + " (2)"))
    except Exception as e:
        print(source_path, destination_path)
        print(f"An unexpected error occurred: {e}")


def create_folder(folder_path, test=False):
    try:  # if os.path.isfile(file_path):
        # Create the directory
        if os.path.isdir(folder_path):
            print(f"Folder {folder_path} already existed")
        else:
            os.makedirs(folder_path, exist_ok=True)
            if test:
                print(f"Folder created successfully at {folder_path}")

    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")


def write_txt_file(txt_path, lines, test=False):
    try:
        if os.path.isfile(txt_path):
            print(f"Folder {txt_path} already exists")
        else:
            # Open the file in write mode and automatically close it using 'with'
            with open(txt_path, "w") as file:
                for line in lines:
                    file.write(line + "\n")
                if test:
                    print(f"File '{txt_path}' has been created successfully.")

    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")


def append_lines(txt_path, lines, test=False):
    try:  # if os.path.isfile(file_path):
        # Open the file in write mode and automatically close it using 'with'
        with open(txt_path, "a") as file:
            for line in lines:
                file.write(line + "\n")
            if test:
                print(f"File '{file_path}' has been created successfully.")

    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")


def remove_empty_folder(folder_path, test=False):
    try:
        if os.path.isdir(folder_path):
            os.rmdir(folder_path)
            if test:
                print(f"Empty folder deleted successfully at {folder_path}")
        else:
            print(f"Folder {folder_path} doesn't exist")

    except OSError as e:
        print(f"Error: {folder_path} : {e.strerror}")


# From a set of languages et subtitles, bool : is it vost and not french ?
# Arguments should be lists
def is_vost(languages, subtitles):
    return len(list(set(languages))) >= 2 and len(subtitles) >= 1


def is_video(file_path):
    return u.get_extension(file_path).lower() in POSSIBLE_EXTENSIONS and os.path.isfile(
        file_path
    )


def is_film(file_path):
    file_size = os.stat(file_path).st_size
    video = is_video(file_path)
    if not video:
        return False
    else:
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "General":
                if track.duration == None:
                    duration = (0, 0, 0)
                else:
                    duration = convert_milliseconds(int(float(track.duration)))
    return duration > (0, 30, 0) and int(file_size) > 500000000




# Exception if it's not a film.
# Register the film row in the database
# Returns the old and new name
# Doesn't register films that already are there
def register(film_path, disk_number, table_name=TABLE_NAME):
    assert is_film(film_path), "you tried to register a file that is not a film."

    duration, languages, subtitles = extract_video_metadata(film_path)

    film_path = Path(film_path)
    film_metadata = get_file_metadata(film_path)
    film_metadata = film_metadata + "   " + duration

    old_film_title = film_path.name
    new_film_title = text_formatter(old_film_title)
    vost = is_vost(languages, subtitles)

    row = [
        film_metadata,
        new_film_title,
        disk_number,
        duration,
        vost,
        ", ".join(languages),
        ", ".join(subtitles),
        old_film_title,
    ]

    if db.is_in_table(DB_NAME, table_name, COLUMNS, film_metadata):
        old_film = db.get_row_film_metadata(DB_NAME, table_name, COLUMNS, film_metadata)
        if (
            old_film.Film_title != new_film_title
            and old_film.Disk_number.split(", ")[0] == disk_number
        ):  # On change le titre s'il a été changé dans le disque dur initial.
            db.change_row(
                DB_NAME,
                table_name,
                COLUMNS,
                film_metadata,
                "Film_title",
                new_film_title,
            )
        if disk_number not in old_film.Disk_number.split(", "):
            db.change_row(
                DB_NAME,
                table_name,
                COLUMNS,
                film_metadata,
                "Disk_number",
                old_film.Disk_number + ", " + disk_number,
            )
    else:
        row = [[row[i], COLUMNS[i][1]] for i in range(len(row))]
        db.add_row(DB_NAME, table_name, COLUMNS, row)

    return old_film_title, new_film_title, film_metadata


# This function treats files when there's no group effect.
# It means that
# It :
# Puts in Other if file and not film .
# Puts at the root and rename the file name if it's a film
# and registers its information in the db if it's a film.
# If it is a folder, it also moves it in Other

# It only works ON FILES AND in the following cases :
# - the file is a film
# - the folder contains some films.
# No test of valid using for the


def simple_treater(
    file_path, disk_number, path_to_disk, reorganise=True, metadata_moved_film_list=[]
):
    film_metadata = None
    if is_film(file_path):
        _, new_film_title, film_metadata = register(file_path, disk_number)
        print(new_film_title)
        print("Path : ", file_path, "\n")

        if reorganise and Path(file_path) != Path(path_to_disk) / new_film_title:
            if film_metadata in metadata_moved_film_list:
                corbeille_path = Path(path_to_disk) / "Corbeille"
                move_and_rename_file(file_path, corbeille_path / Path(file_path).name)
            else:
                move_and_rename_file(file_path, Path(path_to_disk) / new_film_title)
    elif file_path.name not in ["Other", "Corbeille"]:
        file_title = Path(file_path).name  # Works also on folders
        if reorganise:
            move_and_rename_file(file_path, Path(path_to_disk) / "Other" / file_title)
    return film_metadata


def update_to_github(
    file_path, repo_file_path, repo_name, github_username, github_token
):

    # GitHub API endpoint to get the existing file details
    file_url = f"https://api.github.com/repos/{github_username}/{repo_name}/contents/{repo_file_path}"
    # Headers for the request
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    # First, get the existing file details to obtain the SHA
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        file_details = response.json()
        file_sha = file_details["sha"]

        # Read the .db file content in binary mode and encode it in base64
        with open(file_path, "rb") as file:
            db_content = file.read()
        db_content_base64 = base64.b64encode(db_content).decode("utf-8")
        # Data for the request to update the file
        data = {
            "message": "Update .db file using Python",
            "content": db_content_base64,
            "sha": file_sha,  # Include the SHA of the existing file
        }

        # Make a PUT request to update the .db file
        update_response = requests.put(file_url, headers=headers, json=data)

        if update_response.status_code == 200:
            print(f"File '{repo_file_path}' updated successfully.")
        else:
            print(f"Failed to update file. Status code: {update_response.status_code}")
            print(update_response.json())
    else:
        print(f"Failed to get file details. Status code: {response.status_code}")
        print(response.json())


def get_file_metadata(file_path):
    # Récupérer les métadonnées du fichier
    stat_info = os.stat(file_path)

    metadata = {
        "taille": stat_info.st_size,
    }

    return str(metadata["taille"])


if __name__ == "__main__":
    # Example usage
    file_path = "C:\\colin_films\\Dersou.Ouzala\\Dersou.Ouzala.mkv"
    extract_video_metadata(file_path, test=True)
    test_str = "Hello I'm COLIN. DROUINEAU 1253.MIDJ .mkv"
    text_formatter(test_str, test=True)
