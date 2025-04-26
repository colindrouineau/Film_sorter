from pymediainfo import MediaInfo
from CONFIG import *
import os
import shutil
import utils as u
import db


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
            duration = convert_milliseconds(track.duration)
            duration = (
                str(duration[0])
                + " h "
                + str(duration[1])
                + " m "
                + str(duration[2])
                + " s "
            )
        elif track.track_type == "Audio":
            languages.append(track.other_language[0])
        elif track.track_type == "Text":
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
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def create_folder(folder_path, test=False):
    try:  # if os.path.isfile(file_path):
        # Create the directory
        if os.path.isdir(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            if test:
                print(f"Folder created successfully at {folder_path}")
        else:
            print(f"Folder {folder_path} already existed")

    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")


def delete_empty_folder(folder_path, test=False):
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


# Exception if it's not a film.
# Register the film row in the database
def register(film_path, disk_number):
    assert (
        u.get_extension(film_path).lower() not in POSSIBLE_EXTENSIONS
    ), "you tried to register a file that is not a film."

    duration, languages, subtitles = extract_video_metadata(film_path)

    path_seps = ["/", "\\"]
    film_path_list = film_path
    for path_sep in path_seps:
        film_path_list = film_path_list.split(path_seps)
    old_film_title = film_path_list[-1]
    new_film_title = text_formatter()
    vost = is_vost(languages, subtitles)

    row = [
        new_film_title,
        disk_number,
        duration,
        vost,
        ", ".join(languages),
        ", ".join(subtitles),
        old_film_title,
    ]
    db.add_row(DB_NAME, TABLE_NAME, COLUMNS_TITLES, row)


# In case films are mixed with other files in the folder
# Or in case the folder only contains non films objects.
# The hereby function does not test anything.
# It :
# Puts in Other if not film .
# Puts at the root and rename the file name
# and registers its information in the db if it's a film.
def simple_treater(file_path):
    class bo:
        pass


if __name__ == "__main__":
    # Example usage
    file_path = "C:\\colin_films\\Dersou.Ouzala\\Dersou.Ouzala.mkv"
    extract_video_metadata(file_path, test=True)
    test_str = "Hello I'm COLIN. DROUINEAU 1253.MIDJ .mkv"
    text_formatter(test_str, test=True)
