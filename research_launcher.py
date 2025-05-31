import research_utils as ru
from utils import coloured_print as cprint
import db
from CONFIG import *


if __name__ == "__main__":
    print(
        "Quel est le titre du film que vous voulez voir ? Appuyez sur entrée pour la sélection seulement par la durée."
    )
    title = input()
    if title == "":
        title = None
    c = ""
    print("Voulez-vous filter par la durée du film (o/n)")
    while c not in ["n", "o"]:
        c = input()
    if c == "n":
        duration = False
    if c == "o":
        duration = True
        print("Durée minimale ? (format : 1h30)")
        minimum_duration = input()
        print("Durée maximale ? (format : 1h30)")
        maximum_duration = input()

    research_results = db.user_query(
        DB_NAME,
        TABLE_NAME,
        COLUMNS,
        film_title=title,
        film_duration=(minimum_duration, maximum_duration) if duration else None,
    )

    print("Voici le(s) résultat(s) le(s) plus pertinent(s) pour votre recherche :\n")
    rank = len(research_results)
    for research_result in research_results[::-1]:
        cprint(str(rank) + ")  " + research_result.Film_title)
        rank -= 1
        print("Disk_number : ", research_result.Disk_number)
        print("Pistes de langages : ", research_result.Languages)
        print("Pistes de sous-titres : ", research_result.Subtitles)
        print("Durée : ", research_result.Film_duration)
        print()

    print("Pour quitter ce programme, appuyer sur entrée.")
    end = input()
