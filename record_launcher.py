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

    txt_path = Path(path_to_disk) / "Other" / "Film_sorter.txt"
    if os.path.is_file(txt_path):     
        assert disk_number in Disk_Numbers, "The disk should have been registered. Send a request to the developper."
    else:
        rc.create_folder(Path(path_to_disk) / "Other")
        lines = ["Film_sorter"]
        lines.append("")
        lines.append("Numéro de disque : ")
        lines.append(disk_number)
        lines.append("")
        rc.create_txt_file(txt_path, lines)
    
    current_dateTime = str(datetime.now())
    lines = ["Record ", current_dateTime]
    rc.append_lines(txt_path, lines)


    # How to detect it's new : mettre dans "Other" un fichier txt "testé", avec :
    # Je juge que c'est pas nécessaire : Le nombre de films dans le disque, le code pour revenir à la config initiale (ainsi que les titres),
    # Date du record
    # Name of the matching registered disk



    # fonction qui parcourt et arrange tout, et en même temps que le parcours, remplit la base de données
    # la fonction doit aussi écrire le fichier "testé"

    # on fait un premier passage où on traite les films,
    # et un deuxième passage où on balance tout ce qu'est pas film dans Other


def record(path_to_disk, disk_number):
    recorded_films = []

    # List all files and directories in the specified path
    entries = os.listdir(path_to_disk)

    # First
    pile = [path_to_disk / entry for entry in entries]
    while len(pile) > 0:
        treated_path = pile.pop()
        if rc.is_film(treated_path):
            film_name = rc.text_formatter(treated_path.name)
            other_disk_film_name = "Disk " + disk_number + " : " + film_name
            recorded_films.append(film_name)
            recorded_films.append(other_disk_film_name)
            rc.simple_treater(treated_path, disk_number)
        elif os.path.isdir(treated_path):
            entries = os.listdir(treated_path)
            pile += [treated_path / entry for entry in entries]

    # Second
    entries = os.listdir(path_to_disk)

    pile = [path_to_disk / entry for entry in entries]
    while len(pile) > 0:
        treated_path = pile.pop()
        if not rc.is_film(treated_path):
            rc.simple_treater(treated_path, disk_number)

    # Delete if it was deleted on the considered disk.
    # Delete if 2 names of the same film for one disk
    disk_films = db.disk_number_query(DB_NAME, TABLE_NAME, COLUMNS, disk_number)
    for film_title in disk_films:
        disked = "Disk " + disk_number + " : " + film_title
        undisked = (
            film_title[8 + len(disk_number) :]
            if len(film_title) > 8 + len(disk_number)
            else None
        )
        if film_title not in recorded_films:
            db.delete_row(DB_NAME, TABLE_NAME, COLUMNS, film_title)
        elif disked in disk_films and film_title in disk_films:
            db.delete_row(DB_NAME, TABLE_NAME, COLUMNS, disked)
        elif undisked in disk_films and film_title in disk_films:
            db.delete_row(DB_NAME, TABLE_NAME, COLUMNS, film_title)


if __name__ == "__main__":
    print("Vous êtes sur le point d'enregistrer votre disque dur sur Film_sorter. Il sera réagencé et vous ne pourrez pas retourner à l'agencement initial.")
    print("Voulez-vous continuer ? (o/n)")
    start = input()
    if start == "o" :
        print('Quelle est la lettre de lecteur de votre disque dur ?')
        path_to_disk = Path(input().upper + ":")
        txt_path = path_to_disk / "Other " / "Film_sorter.txt"
        if os.path.is_file(txt_path):
            with open(txt_path, 'r') as file:
                contents = file.read()
                lines = contents.splitlines()
                disk_number = lines[3]      
            print("Le numéro d'identification de votre disque dur est : ", disk_number)
        else:
            print("Quel numéro d'identification voulez-vous donner à votre disque ?")
            disk_number = input()
        initialise(path_to_disk, disk_number)
        record(path_to_disk, disk_number)
    else:
        print("Nous espérons vous revoir bientôt.")