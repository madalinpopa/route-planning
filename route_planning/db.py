from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

engine = create_engine("sqlite:///route_planning.sqlite")
db_session = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import route_planning.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
