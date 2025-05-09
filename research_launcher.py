import research_utils as ru
import utils as u
import db
from CONFIG import *


if __name__ == "__main__":
    print("what is the title")
    title = "hte brutalist"  # input()
    print("minimum duration ? (1h30m)")
    minimum_duration = "1"  # u.hms_to_tuple(input())
    # print("max ?")
    maximum_duration = "30"  # u.hms_to_tuple(input())

    research_results = db.user_query(
        DB_NAME,
        TABLE_NAME,
        COLUMNS,
        film_title=title,
        film_duration=(minimum_duration, maximum_duration),
    )

    print([research_result.Film_title for research_result in research_results])
