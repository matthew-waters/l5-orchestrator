from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orchestrator.config.settings import Settings


def create_session_factory(settings: Settings):
    engine = create_engine(settings.db_url, future=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
