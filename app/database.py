import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Si existe la variable de entorno DATABASE_URL, la usamos (sirve para Render/Postgres)
# Si no, usamos SQLite en un archivo local llamado personas.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./personas.db")

# Para SQLite hay que pasar connect_args, para otros motores no
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
