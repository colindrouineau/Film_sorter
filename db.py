from sqlalchemy import create_engine, Column, Integer, String, and_, or_, desc, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from research_utils import significant_str_distance
from record_utils import text_formatter
from utils import coloured_print as cprint
from CONFIG import *


# columns = list of [name str, value type]
def define_classe(db_name, columns, table_name):
    # Create the engine (connects to the database)
    engine = create_engine("sqlite:///" + db_name + ".db")
    Base = declarative_base()
    # Dynamically create column attributes
    # Film_title (First item of columns) must be the primary key
    column_definitions = {
        columns[i][0]: Column(columns[i][1], primary_key=(i == 0)) for i in range(len(columns))
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
def is_in_table(db_name, table_name, column_names, row_id):
    engine, _, User = define_classe(db_name, column_names, table_name)
    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()
    row_id = text_formatter(row_id)

    return session.query(User).filter(User.film_name == row_id).first() is not None


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
# film_duration is a couple (min, max), with min and max = (hours, minutes, seconds)
# VO is a bool
# return the lines of the films that correspond most
# Il me semble que ça renvoie les lignes sous la forme d'une liste.
def query(
    db_name,
    table_name,
    columns,
    film_title,
    film_duration=None,
    VO=None,
):
    engine, _, User = define_classe(db_name, columns, table_name)

    Session = sessionmaker(bind=engine)
    session = Session()

    request_result = (
        session.query(User)
        .filter(
            and_(
                significant_str_distance(film_title, User.film_title) > MIN_STR_DIST,
                User.film_duration > film_duration[0],
                User.film_duration > film_duration[1],
                VO=VO,
            )
        )
        .order_by(desc(significant_str_distance(film_title, User.film_title)))
        .all()
    )

    session.close()

    return request_result


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
    # Convert the result to a list
    column_values = [row[0] for row in result]

    return column_values
