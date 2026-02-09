from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Handling the postgres dialect in case it's mostly compatible with other drivers if needed
# but 'psycopg2' is standard for sync.
# For serverless setups like Neon, connection pooling is important but basic setup:

# Handle both PostgreSQL and SQLite
engine_args = {"echo": True}

if settings.DATABASE_URL.startswith("postgresql"):
    connection_string = settings.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    engine_args.update({
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 10
    })
else:
    connection_string = settings.DATABASE_URL
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(connection_string, **engine_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
