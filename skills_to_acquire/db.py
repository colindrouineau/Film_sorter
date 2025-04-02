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


# row = list of [name str, value type]
def define_classe(db_name, row, table_name):
    # Create the engine (connects to the database)
    engine = create_engine("sqlite:///" + db_name + ".db")
    Base = declarative_base()

    # Dynamically create column attributes
    # Date (First item of columns) must be the primary key
    column_definitions = {
        row[i][0]: Column(row[i][1], primary_key=(i == 0)) for i in range(len(row))
    }
    column_definitions["__tablename__"] = table_name

    # Define the table as a Python class
    User = type("User", (Base,), column_definitions)

    return engine, Base, User


# row = list of [name str, value type]
def create_new_table(db_name, row, table_name):
    # Creates the class from the arguments.
    engine, Base, User = define_classe(db_name, row, table_name)
    # Create the table in the database
    Base.metadata.create_all(engine)


# Row = columns title, questions. Only corresponding questions should be selected
# answer_row = answers
def add_row(db_name, table_name, row, answer_row):

    assert len(row) == len(answer_row), "One question should match one answer."

    # Creates the class from the arguments.
    engine, _, User = define_classe(db_name, row, table_name)

    # Créer une session
    Session = sessionmaker(bind=engine)
    session = Session()

    attribute_values = {row[i][0]: answer_row[i][0] for i in range(len(answer_row))}
    # Instancier dynamiquement la classe User avec les valeurs d'attributs
    new_user = User(**attribute_values)

    # Ajouter l'utilisateur à la session et valider la transaction
    session.add(new_user)
    session.commit()
    # Fermer la session
    session.close()


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
    alice = session.query(User).filter_by(name='Alice').first()

    session.close()