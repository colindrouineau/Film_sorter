from pymediainfo import MediaInfo
from CONFIG import *


def convert_milliseconds(milliseconds):
    # Calculate total seconds
    total_seconds = milliseconds // 1000

    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds


# return duration as (hours, minutes, seconds), languages and subtitles as a list of the available ones.
def extract_mkv_metadata(file_path, test=False):
    media_info = MediaInfo.parse(file_path)
    duration = None
    languages = []
    subtitles = []

    for track in media_info.tracks:
        if track.track_type == "General":
            duration = convert_milliseconds(track.duration)
        elif track.track_type == "Audio":
            languages.append(track.other_language[0])
        elif track.track_type == "Text":
            subtitles.append(track.other_language[0])

    if test:
        print(f"Duration: {duration}")
        print(f"audio : {languages}")
        print(f"subtitles : {subtitles}")

    return duration, languages, subtitles


def punctuation_split(text):
    splitting = []
    word = ""
    for c in text:
        if c in PUNCTUATION:
            if word != "":
                splitting.append(word)
            word = ""
        else:
            word += c
    if word != "":
        splitting.append(word)
    return splitting


def text_formatter(text, test=False):
    punc_sep = punctuation_split(text)
    extension = punc_sep.pop()
    formatted_text = " ".join(punc_sep)
    formatted_text += "." + extension
    # First letter in capital
    formatted_text = formatted_text[0].upper() + formatted_text[1:].lower()
    if test:
        print(formatted_text)
    return formatted_text


from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    MetaData,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship


# column_names = list of [name str, value type]
def define_classe(db_name, column_names, table_name):
    # Create the engine (connects to the database)
    engine = create_engine("sqlite:///" + db_name + ".db")
    Base = declarative_base()

    # Dynamically create column attributes
    # Date (First item of columns) must be the primary key
    column_definitions = {
        column_names[i][0]: Column(column_names[i][1], primary_key=(i == 0))
        for i in range(len(column_names))
    }
    column_definitions["__tablename__"] = table_name

    # Define the table as a Python class
    User = type("User", (Base,), column_definitions)

    return engine, Base, User


# column_names = list of [name str, value type]
def create_new_table(db_name, column_names, table_name):
    # Creates the class from the arguments.
    engine, Base, _ = define_classe(db_name, column_names, table_name)
    # Create the table in the database
    Base.metadata.create_all(engine)


# column_names = list of [name str, value type]
# column_names = columns title, questions. Only corresponding questions should be selected
# answer_row = answers
def add_row(db_name, table_name, column_names, added_row):

    assert len(column_names) == len(added_row), "a column should fit a value"

    # Creates the class from the arguments.
    engine, _, User = define_classe(db_name, column_names, table_name)

    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()

    attribute_values = {
        column_names[i][0]: added_row[i][0] for i in range(len(added_row))
    }
    # Instancier dynamiquement la classe User avec les valeurs d'attributs
    new_user = User(**attribute_values)

    # Ajouter l'utilisateur à la session et valider la transaction
    session.add(new_user)
    session.commit()
    # Fermer la session
    session.close()


# Fonction pour vérifier si un élément existe
def is_in_table(db_name, table_name, column_names, row_id):
    engine, _, User = define_classe(db_name, column_names, table_name)

    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session.query(User).filter(User.film_name == row_id).first() is not None


# For the moment, I don't use the following functions. I will fix them when I need them.


def get_column_keys(db_name, table_name):
    # Create a session (allows interaction with the database)
    engine = create_engine("sqlite:///" + db_name + ".db")
    # Initialize MetaData
    metadata = MetaData()
    # Reflect the table you want
    table = Table(table_name, metadata, autoload_with=engine)
    # Print table columns (optional, for verification)
    return table.columns.keys()


def get_rows(db_name, table_name):
    # Create a session (allows interaction with the database)
    engine = create_engine("sqlite:///" + db_name + ".db")
    # Initialize MetaData
    metadata = MetaData()
    # Reflect the table you want
    table = Table(table_name, metadata, autoload_with=engine)
    # Query the table
    with Session(engine) as session:
        result = session.execute(table.select()).fetchall()
    return result


# selecting some specific items (to put in another function)
#    db.select([films]).where(db.and_(films.columns.certification == 'R',
#                                     films.columns.release_year > 2003))


def query():
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query all users
    users = session.query(User).all()

    # Query users with a specific name
    alice = session.query(User).filter_by(name="Alice").first()

    session.close()


if __name__ == "__main__":
    # Example usage
    file_path = "C:\\colin_films\\Dersou.Ouzala\\Dersou.Ouzala.mkv"
    extract_mkv_metadata(file_path, test=True)
    test_str = "Hello I'm COLIN. DROUINEAU 1253.MIDJ .mkv"
    text_formatter(test_str, test=True)
