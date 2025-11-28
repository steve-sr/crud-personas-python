from sqlalchemy import Column, Integer, String

from .database import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    apellido = Column(String, index=True, nullable=False)
    email = Column(String, nullable=True)
