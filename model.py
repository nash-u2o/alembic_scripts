import os

import alembic.command as ac
import pandas as pd
from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    inspect,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .alembic_scripts import (
    alembic_engine,
    alembic_location,
    alembic_revision,
    delete_alembic_migrations,
)
from .app import Test as app

Session = app.get_persistent_store_database("place_db", as_sessionmaker=True)
Base = declarative_base()


class District(Base):
    __tablename__ = "districts"

    fid = Column(Integer, primary_key=True)
    disturl = Column(Text)
    party = Column(Text)
    distname = Column(Text)
    repname = Column(Text)  # Added after data initial data insertion. Migrated in


def db_initializer(engine, first_time):
    ini_path = "/tethysdev/tethysapp-test/tethysapp/test/alembic.ini"
    directory_path = "/tethysdev/tethysapp-test/tethysapp/test/alembic"

    if first_time:
        # Delete old migrations so they don't cause any exceptions
        delete_alembic_migrations(directory_path=directory_path)

        Base.metadata.create_all(engine)

        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()

        # Insert some tuples here

        session.commit()
        session.close()
    else:
        alembic_engine(
            engine=engine,
            ini_path=ini_path,
        )
        alembic_location(
            ini_path=ini_path,
            directory_path=directory_path,
        )
        alembic_revision(ini_path=ini_path)


def merge_data(engine, abs_path):
    abs_path = os.path.abspath(abs_path)
    if os.path.exists(abs_path):
        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()
        data = pd.read_csv(abs_path)
        for index, row in data.iterrows():
            session.merge(
                District(
                    fid=row["FID"],
                    disturl=row["DISTURL"],
                    party=row["PARTY"],
                    distname=row["DISTNAME"],
                    repname=row["REPNAME"],  # new row
                )
            )
        session.commit()
        session.close()
    else:
        print(f"Invalid path '{abs_path}'")
