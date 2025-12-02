from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import Base, SessionLocal, engine

from fastapi import BackgroundTasks
from . import email_utils

# Crear tablas en la BD (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD de Personas", version="1.0.0")

# CORS para que Netlify pueda llamar a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependencia para obtener una sesión de BD en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================
# ENDPOINTS (CRUD)
# ==========================

@app.get("/personas", response_model=List[schemas.Persona])
def listar_personas(db: Session = Depends(get_db)):
    return crud.get_personas(db)


@app.get("/personas/{persona_id}", response_model=schemas.Persona)
def obtener_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = crud.get_persona(db, persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


@app.post("/personas", response_model=schemas.Persona, status_code=201)
def crear_persona(
    persona: schemas.PersonaCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    nueva_persona = crud.create_persona(db, persona)

    if persona.email:
        background_tasks.add_task(
            email_utils.send_welcome_email,
            to_email=persona.email,
            nombre=persona.nombre,
        )

    return nueva_persona

@app.put("/personas/{persona_id}", response_model=schemas.Persona)
def actualizar_persona(
    persona_id: int,
    datos_actualizacion: schemas.PersonaUpdate,
    db: Session = Depends(get_db),
):
    persona = crud.update_persona(db, persona_id, datos_actualizacion)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


@app.delete("/personas/{persona_id}", status_code=204)
def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_persona(db, persona_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return None
