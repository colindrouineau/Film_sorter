from sqlalchemy import (
    create_engine,
    Column,
    String,
    and_,
    or_,
    desc,
    MetaData,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from research_utils import significant_str_distance
from utils import coloured_print as cprint, hms_to_tuple
from CONFIG import *


# columns = list of [name str, value type]
def define_classe(db_name, columns, table_name):
    # Create the engine (connects to the database)
    engine = create_engine("sqlite:///" + db_name + ".db")
    Base = declarative_base()
    # Dynamically create column attributes
    # Film_title (First item of columns) must be the primary key
    column_definitions = {
        columns[i][0]: Column(columns[i][1], primary_key=(i == 0))
        for i in range(len(columns))
    }
    column_definitions["__tablename__"] = table_name
    # Define the table as a Python class
    User = type("User", (Base,), column_definitions)

    return engine, Base, User


# columns = list of [name str, value type]
# Creates new table if it does not already exist.
def create_new_table(db_name, columns, table_name):
    # Creates the class from the arguments.
    engine, Base, _ = define_classe(db_name, columns, table_name)
    # Create the table in the database
    Base.metadata.create_all(engine)


# Fonction pour vérifier si un élément existe (le titre doit être identique pour que l'élément soit reconnu)
def is_in_table(db_name, table_name, columns, row_id):
    engine, _, User = define_classe(db_name, columns, table_name)
    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(User).filter(User.Film_metadata == row_id).first() is not None


def film_title_in_table(db_name, table_name, columns, film_title):
    engine, _, User = define_classe(db_name, columns, table_name)
    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(User).filter(User.Film_title == film_title).first() is not None


# columns = columns title, questions. Only corresponding questions should be selected
# row = answers
def add_row(db_name, table_name, columns, row):
    assert len(columns) == len(row), "One question should match one answer."

    # Creates the class from the arguments.
    engine, _, User = define_classe(db_name, columns, table_name)

    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()

    attribute_values = {columns[i][0]: row[i][0] for i in range(len(row))}
    # Instancier dynamiquement la classe User avec les valeurs d'attributs
    new_user = User(**attribute_values)

    # Ajouter l'utilisateur à la session et valider la transaction
    session.add(new_user)
    session.commit()
    # Fermer la session
    session.close()


# A TESTER POSSIBLE ECHEC
# film_title is a string
# film_duration is a couple (min, max), with min and max = "hh h mm m ss s"  (flexible format)
# VO is a bool
# return the lines of the films that correspond most
# Il me semble que ça renvoie les lignes sous la forme d'une liste.
def user_query(db_name, table_name, columns, film_title=None, film_duration=None):
    if film_duration == None:
        film_duration = [(0, 0, 0), (10, 0, 0)]
    else:
        film_duration = [hms_to_tuple(film_duration[0]), hms_to_tuple(film_duration[1])]

    engine, _, User = define_classe(db_name, columns, table_name)

    Session = sessionmaker(bind=engine)
    session = Session()
    # Filter the results in Python :
    request_result = session.query(User).all()
    request_result = [
        user
        for user in request_result
        if hms_to_tuple(user.Film_duration) > film_duration[0]
        and hms_to_tuple(user.Film_duration) < film_duration[1]
    ]
    request_result = sorted(
        request_result, key=lambda user: hms_to_tuple(user.Film_duration)
    )
    if film_title == None:
        selected_request_result = request_result
    else:
        request_result = sorted(
            request_result,
            key=lambda user: significant_str_distance(user.Film_title, film_title),
            reverse=True,
        )
        selected_request_result = request_result[: min(len(request_result), 3)]
        i = 0
        while (
            3 + i < len(request_result)
            and significant_str_distance(request_result[0].Film_title, film_title)
            - significant_str_distance(request_result[3 + i].Film_title, film_title)
            <= 10
        ):
            selected_request_result.append(request_result[3 + i])
            i += 1
            # Ne pas écarter des résultats qui resteraient pertinents
            # (Je pense aux sagas par exemple)
    session.close()

    return selected_request_result


def get_column_as_list(db_name, table_name, columns, column_name):
    engine, _, _ = define_classe(db_name, columns, table_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Reflect the existing database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Access the existing table
    if table_name in metadata.tables:
        users = metadata.tables[table_name]
        table = users
    else:
        raise ValueError(f"Table '{table_name}' does not exist in the database.")

    if column_name not in table.c:
        raise ValueError(
            f"La colonne '{column_name}' n'existe pas dans la table '{table.name}'"
        )

    # Execute a query to get the values of the column
    result = session.query(table.c[column_name]).all()
    session.close()
    # Convert the result to a list
    column_values = [row[0] for row in result]

    return column_values


def delete_missing_films(db_name, table_name, columns, disk_number, recorded_films):
    engine, _, User = define_classe(db_name, columns, table_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User).all()
    session.close()

    for user in result:
        splitted = user.Disk_number.split(", ")
        if disk_number in splitted:
            if user.Film_metadata not in recorded_films:
                if len(splitted) == 1:
                    delete_row(db_name, table_name, columns, user.Film_metadata)
                else:
                    new_disk_number = [dn for dn in splitted if dn != disk_number]
                    new_disk_number = ", ".join(new_disk_number)
                    change_row(
                        db_name,
                        table_name,
                        columns,
                        user.Film_metadata,
                        "Disk_number",
                        new_disk_number,
                    )


def get_disk_metadata(db_name, table_name, columns, disk_number):
    engine, _, User = define_classe(db_name, columns, table_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.query(User).all()
    session.close()

    metadata_list = []
    for user in result:
        splitted = user.Disk_number.split(", ")
        if disk_number in splitted:
            metadata_list.append(user.Film_metadata)
    return metadata_list


def delete_row(db_name, table_name, columns, film_metadata):
    engine, _, User = define_classe(db_name, columns, table_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Query the row you want to delete (e.g., by primary key)
    film_to_delete = (
        session.query(User).where(User.Film_metadata == film_metadata).first()
    )
    if film_to_delete:
        session.delete(film_to_delete)
        session.commit()
        session.close()


# Renvoie une instance de la calsse User.
def get_row_film_title(db_name, table_name, columns, film_title):
    engine, _, User = define_classe(db_name, columns, table_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Query the row you want to delete (e.g., by primary key)
    film_row = session.query(User).where(User.Film_title == film_title).first()
    session.close()
    return film_row


def get_row_film_metadata(db_name, table_name, columns, film_metadata):
    engine, _, User = define_classe(db_name, columns, table_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    # Query the row you want to delete (e.g., by primary key)
    film_row = session.query(User).where(User.Film_metadata == film_metadata).first()
    session.close()
    return film_row


def change_row(
    db_name, table_name, columns, row_id, attribute, new_attribute_value, test=False
):
    engine, _, User = define_classe(db_name, columns, table_name)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Query the row you want to update
        row = session.query(User).filter_by(Film_metadata=row_id).first()

        if row:
            # Dynamically set the attribute
            if hasattr(row, attribute):
                setattr(row, attribute, new_attribute_value)
                session.commit()
                if test:
                    print(f"Row {row_id} updated successfully.")
            elif test:
                print(f"Attribute '{attribute}' does not exist.")
        elif test:
            print(f"Row with id {row_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()
