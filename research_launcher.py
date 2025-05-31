import research_utils as ru
from utils import coloured_print as cprint
import db
from CONFIG import *


if __name__ == "__main__":
    print("Quel est le titre du film que vous voulez voir ?")
    title = input()
    c = ""
    while c not in ["n", "o"]:
        print("Voulez-vous filter par la durée du film (o/n)")
    if c == "n":
        duration = False
    if c == "o":
        duration = True
        print("Durée minimale ? (format : 1h30m)")
        minimum_duration = input()
        print("Durée maximale ? (format : 1h30m)")
        maximum_duration = input()

    research_results = db.user_query(
        DB_NAME,
        TABLE_NAME,
        COLUMNS,
        film_title=title,
        film_duration=(minimum_duration, maximum_duration) if duration else None,
    )

    print("Voici les 3 résultats les plus pertinents pour votre recherche :")
    for research_result in research_results:
        cprint(research_result.Film_title)
        print("Disk_number : ", research_result.Disk_number)
        print("Pistes de langages : ", research_result.Languages)
        print("Pistes de sous-titres : ", research_result.Subtitles)
        print()

    print("Pour quitter ce programme, appuyer sur entrée.")
    end = input()
