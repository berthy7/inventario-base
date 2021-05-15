from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

SessionMaker = None
db_url = None


def get_session():
    global SessionMaker
    global db_url

    if SessionMaker is None:
        SessionMaker = sessionmaker(bind=create_engine(db_url), expire_on_commit=False, autoflush=False)
    return SessionMaker()


@contextmanager
def transaction():
    """Provide a transactional scope around a series of operations."""
    global SessionMaker
    global db_url

    if SessionMaker is None:
        SessionMaker = sessionmaker(bind=create_engine(db_url), expire_on_commit=False, autoflush=False)
    session = SessionMaker()

    try:
        yield session
    except Exception as e:
        print(e)
        session.rollback()
        raise
    finally:
        session.close()
