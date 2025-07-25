from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from shared.config import settings

DATABASE_URL = f"postgresql://{settings.postgresql_user}:{settings.postgresql_password}@{settings.postgresql_server}:{settings.postgresql_port}/{settings.postgresql_name}"

engine = create_engine(DATABASE_URL, echo=settings.debug)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()