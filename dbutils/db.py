from sqlmodel import SQLModel, create_engine
from . import models

engine = create_engine("sqlite:///lidcode.db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)