from CONFIG import *
import os
import db
import utils as u
import record_utils as rc
from pathlib import Path
from datetime import datetime


# Renvoie True si le disque dur avait déjà été enregistré, False s'il est nouveau.
def initialise(path_to_disk, disk_number):
    db.create_new_table(
        DB_NAME, COLUMNS, TABLE_NAME
    )  # Creation of the db if not already there

    Disk_Numbers = db.get_column_as_list(DB_NAME, TABLE_NAME, COLUMNS, "Disk_number")
    Disk_Numbers = list(set(Disk_Numbers))
    txt_path = Path(path_to_disk) / "Other" / "Film_sorter.txt"
    if os.path.isfile(txt_path):
        if disk_number not in Disk_Numbers:
            warning = (
            "You have no film recorded for this disk. \nHere are the registered disk_numbers : "
            + str(Disk_Numbers)
        )
            u.coloured_print(warning, "red")
    else:
        rc.create_folder(Path(path_to_disk) / "Other")
        lines = ["Film_sorter"]
        lines.append("")
        lines.append("Numéro de disque : ")
        lines.append(disk_number)
        lines.append("")
        lines.append("Records : ")
        rc.write_txt_file(txt_path, lines)

    current_dateTime = str(datetime.now())[:-7]
    lines = [current_dateTime]
    rc.append_lines(txt_path, lines)

    # How to detect it's new : mettre dans "Other" un fichier txt "testé", avec :
    # Je juge que c'est pas nécessaire : Le nombre de films dans le disque, le code pour revenir à la config initiale (ainsi que les titres),
    # Date du record
    # Name of the matching registered disk

    # fonction qui parcourt et arrange tout, et en même temps que le parcours, remplit la base de données
    # la fonction doit aussi écrire le fichier "testé"

    # on fait un premier passage où on traite les films,
    # et un deuxième passage où on balance tout ce qu'est pas film dans Other


def record(path_to_disk, disk_number, reorganise=True):
    recorded_films = []

    # List all files and directories in the specified path
    entries = os.listdir(path_to_disk)

    # First
    pile = [path_to_disk / entry for entry in entries]
    while len(pile) > 0:
        treated_path = pile.pop()
        if rc.is_film(treated_path):
            film_name = rc.text_formatter(treated_path.name)
            recorded_films.append(film_name)
            rc.simple_treater(treated_path, disk_number, path_to_disk, reorganise=reorganise)
        elif os.path.isdir(treated_path):
            entries = os.listdir(treated_path)
            pile += [treated_path / entry for entry in entries]

    # Second
    entries = os.listdir(path_to_disk)

    pile = [path_to_disk / entry for entry in entries]
    while len(pile) > 0:
        treated_path = pile.pop()
        if not rc.is_film(treated_path):
            rc.simple_treater(treated_path, disk_number, path_to_disk)

    # Delete if it was deleted on the considered disk.
    # Delete if 2 names of the same film for one disk
    disk_films = db.disk_number_query(DB_NAME, TABLE_NAME, COLUMNS, disk_number)
    for film_title in disk_films:
        if film_title not in recorded_films:
            db.delete_row(DB_NAME, TABLE_NAME, COLUMNS, film_title)


if __name__ == "__main__":
    # Get the current working directory
    current_path = os.getcwd()

    print(
        "Vous êtes sur le point d'enregistrer votre disque dur sur Film_sorter. \nIl sera réagencé et vous ne pourrez pas retourner à l'agencement initial."
    )
    print("Voulez-vous continuer ? (o/n)")
    start = input()
    if start == "o":
        print("Voulez-vous réorganiser votre disque dur (mettre tous les films à la racine et tout le reste dans un dossier) ? (o/n)")
        reorganise = True if input() == "o" else False
        print(
            "Quelle est la lettre de lecteur de votre disque dur ? (ou le chemin absolu de votre disque dur)"
        )
        path_to_disk = input()
        if len(path_to_disk) == 1:
            path_to_disk = Path(path_to_disk.upper() + ":")
        else:
            path_to_disk = Path(path_to_disk)
        txt_path = path_to_disk / "Other" / "Film_sorter.txt"
        if os.path.isfile(txt_path):
            with open(txt_path, "r") as file:
                contents = file.read()
                lines = contents.splitlines()
                disk_number = lines[3]
            print("Le numéro d'identification de votre disque dur est :", disk_number)
        else:
            print("Quel est le numéro d'identification de votre disque ?")
            disk_number = input()
        initialise(path_to_disk, disk_number)
        record(path_to_disk, disk_number, reorganise=reorganise)

        recorded_paths_path = Path(current_path) / "recorded_paths.txt"
        db_path_ok, token_path_ok = False, False
        if os.path.isfile(recorded_paths_path):
            with open(recorded_paths_path, "r") as file:
                contents = file.read()
                lines = contents.splitlines()
                if lines[0] == "db_path":
                    db_path = lines[1]
                    db_path_ok = True
                if lines[0] == "token_path":
                    token_path = lines[1]
                    token_path_ok = True
                if len(lines) == 4:
                    if lines[2] == "db_path":
                        db_path = lines[3]
                        db_path_ok = True
                    if lines[2] == "token_path":
                        token_path = lines[3]
                        token_path_ok = True
        if os.path.isfile(Path(current_path) / "Film_sorter.db"):
            db_path = Path(current_path) / "Film_sorter.db"
        elif not db_path_ok:
            print("What is the path to Film_sorter.db ?")
            db_path = input()
            print("Voulez-vous enregistrer ce chemin ? (o/n)")
            yesorno = input()
            if yesorno == "o":
                lines = ["db_path", db_path]
                rc.write_txt_file(recorded_paths_path, lines)
        if not token_path_ok:
            print("What is the path to the token ?")
            token_path = input()
            print("Voulez-vous enregistrer ce chemin ? (o/n)")
            yesorno = input()
            if yesorno == "o":
                lines = ["token_path", token_path]
                rc.write_txt_file(recorded_paths_path, lines)

        with open(token_path, "r") as file:
            github_token = file.read()

        repo_file_path = "Film_sorter.db"
        repo_name = "Film_sorter"
        github_username = "colindrouineau"
        rc.update_to_github(
            db_path, repo_file_path, repo_name, github_username, github_token
        )
        print("Pour quitter ce programme, appuyer sur entrée.")
        end = input()

    else:
        print("Nous espérons vous revoir bientôt.")
        print("Pour quitter ce programme, appuyer sur entrée.")
        end = input()
