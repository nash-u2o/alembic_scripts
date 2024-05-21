from geoalchemy2 import Geometry
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .alembic_scripts import alembic_engine, alembic_revision, alembic_suite
from .app import Test as app

Session = app.get_persistent_store_database("place_db", as_sessionmaker=True)
Base = declarative_base()


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)
    geom = Column(Geometry(geometry_type="POINT"))


class NewTable(Base):
    __tablename__ = "new"

    id = Column(Integer, primary_key=True)
    geom = Column(Geometry(geometry_type="LINESTRING"))
    more = Column(Text)
    even_more = Column(ForeignKey("places.id"))
    even_even_more = Column(Boolean)


def db_initializer(engine, first_time):
    Base.metadata.create_all(engine)

    if first_time:
        SessionMaker = sessionmaker(bind=engine)
        session = SessionMaker()

        # Insert some tuples here

        session.commit()
        session.close()
    else:
        # Call the alembic function(s) after the Base.metadata.create_all(engine) call to avoid any issues
        # that may occur if tables are created/deleted

        # Pass absolute path if not calling syncstores in same directory as alembic.ini
        # alembic_engine(engine, "/tethysdev/tethysapp-test/tethysapp/test/alembic.ini")
        # alembic_engine(engine, "alembic.ini") equivalent to alembic_engine(engine)

        alembic_suite(engine, "alembic.ini")
