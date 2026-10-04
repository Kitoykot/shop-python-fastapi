from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.postgresql.settings import database

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{database.db_user}:{database.db_password}"
    f"@{database.db_host}:{database.db_port}"
    f"/{database.db_name}"
)

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
