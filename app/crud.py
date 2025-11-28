from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def get_personas(db: Session) -> List[models.Persona]:
    return db.query(models.Persona).all()


def get_persona(db: Session, persona_id: int) -> Optional[models.Persona]:
    return (
        db.query(models.Persona)
        .filter(models.Persona.id == persona_id)
        .first()
    )


def create_persona(db: Session, persona: schemas.PersonaCreate) -> models.Persona:
    db_persona = models.Persona(
        id=persona.id,
        nombre=persona.nombre,
        apellido=persona.apellido,
        email=persona.email,
    )
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona


def update_persona(
    db: Session, persona_id: int, datos: schemas.PersonaUpdate
) -> Optional[models.Persona]:
    db_persona = get_persona(db, persona_id)
    if db_persona is None:
        return None

    datos_dict = datos.dict(exclude_unset=True)
    for campo, valor in datos_dict.items():
        setattr(db_persona, campo, valor)

    db.commit()
    db.refresh(db_persona)
    return db_persona


def delete_persona(db: Session, persona_id: int) -> bool:
    db_persona = get_persona(db, persona_id)
    if db_persona is None:
        return False

    db.delete(db_persona)
    db.commit()
    return True
