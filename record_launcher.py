import os


def record(path_to_disk, new_name=None):
    # if new disque dur : do you want to rename it ?
    
    # How to detect it's new : mettre dans "Other" un fichier txt "testé", avec :
    # Le nombre de films dans le disque, le code pour revenir à la config initiale (ainsi que les titres), 
    # Date du record

    # fonction qui parcourt et arrange tout, et en même temps que le parcours, remplit la base de données
    # la fonction doit aussi écrire le fichier "testé"



    # List all files and directories in the specified path
    entries = os.listdir(path_to_disk)

    for entry in entries:
        print(entry)


if __name__ == "__main__":
    print()
