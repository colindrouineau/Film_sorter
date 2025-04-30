from CONFIG import *
import os
import db
import utils as u
import record_utils as rc


def initialise(path_to_disk):
    db.create_new_table(
        DB_NAME, COLUMNS, TABLE_NAME
    )  # Creation of the db if not already there

    Disk_Numbers = db.get_column_as_list("Disk_number")
    disk_number = u.punctuation_split(path_to_disk)[-1]

    if disk_number not in Disk_Numbers:
        rc.create_folder(path_to_disk + "\\Other")
        Disk_Numbers_unique = list(set(Disk_Numbers))
        print("here are the different disk_numbers :", Disk_Numbers_unique)
        print("do you want to rename it ?")
        # It is uselessly difficult to rename it. It will have a superficial name in the txt file.
        disk_number = input()
        # Then have to check with .exe method.

    # How to detect it's new : mettre dans "Other" un fichier txt "testé", avec :
    # Le nombre de films dans le disque, le code pour revenir à la config initiale (ainsi que les titres),
    # Date du record
    # Name of the matching registered disk

    # fonction qui parcourt et arrange tout, et en même temps que le parcours, remplit la base de données
    # la fonction doit aussi écrire le fichier "testé"

    # on fait un premier passage où on traite les films,
    # et un deuxième passage où on balance tout ce qu'est pas film dans Other


def record(path_to_disk):
    # List all files and directories in the specified path
    entries = os.listdir(path_to_disk)

    # First
    pile = []
    pile.append(entries)
    while len(pile) > 0:
        treated_path = pile.pop()
        if rc.is_film(treated_path):
            rc.simple_treater(treated_path)
        elif os.path.isdir(treated_path):
            pile.append(os.listdir(treated_path))

    # Second
    pile = []
    pile.append(entries)
    while len(pile) > 0:
        treated_path = pile.pop()
        if not rc.is_film(treated_path):
            rc.simple_treater(treated_path)


if __name__ == "__main__":
    path_to_disk = "c\\Film_sorter_test"

    initialise(path_to_disk)
    record(path_to_disk)
