from typing import Optional

from pydantic import BaseModel


class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    email: Optional[str] = None


class PersonaCreate(PersonaBase):
    id: int


class PersonaUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None


class Persona(PersonaBase):
    id: int

    class Config:
        orm_mode = True
