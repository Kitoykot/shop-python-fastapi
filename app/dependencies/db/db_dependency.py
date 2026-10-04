from collections.abc import Generator

from sqlalchemy.orm import Session

from config.postgresql.connection import SessionFactory


def get_db() -> Generator[Session, None, None]:
    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()
