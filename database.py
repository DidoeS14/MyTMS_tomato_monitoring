import datetime

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base

from config import database_config

Base = declarative_base()


# Define the `growth` table ORM class
class Growth(Base):
    __tablename__ = 'growth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    area = Column(String(100), nullable=False)
    green_count = Column(Integer, default=0)
    half_ripened_count = Column(Integer, default=0)
    fully_ripened_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<Growth(id={self.id}, date={self.date}, area={self.area}, green_count={self.green_count}, " \
               f"half_ripened_count={self.half_ripened_count}, fully_ripened_count={self.fully_ripened_count})>"


class Disease(Base):
    __tablename__ = 'disease'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    area = Column(String(100), nullable=False)
    illness = Column(String(100), nullable=False)
    ill_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<Disease(id={self.id}, date={self.date}, area={self.area}, illness={self.illness}, " \
               f"ill_count={self.ill_count})>"


class Writer:
    def __init__(self):
        self.engine = create_engine(database_config.URL)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        Base.metadata.create_all(self.engine)

    def ping(self):
        self.engine = create_engine(database_config.URL)

        try:
            # Attempt to connect to the database by executing a simple query
            with self.engine.connect() as connection:
                print("Connection to the database was successful!")
        except SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")

    def add_data(self, table, **kwargs):
        """
        Adds data to the specified table.

        Args:
            table: The ORM class representing the table.
            **kwargs: Key-value pairs representing the data to insert.
        """
        try:
            # Dynamically create a new instance of the table with provided data
            record = table(**kwargs)
            self.session.add(record)
            self.session.commit()
            print(f"Successfully added data to {table.__tablename__}: {kwargs}")
        except Exception as e:
            self.session.rollback()
            print(f"Error adding data to {table.__tablename__}: {e}")


writer = Writer()

if __name__ == '__main__':
    writer.add_data(Disease, date=datetime.datetime.now(), area='A', illness='rotting', ill_count=1)

    # Close the session
    writer.session.close()
