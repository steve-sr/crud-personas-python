from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# ==========================
# SCHEMAS (Pydantic models)
# ==========================

class PersonaBase(BaseModel):
    """Campos comunes de persona."""
    nombre: str
    apellido: str
    email: Optional[str] = None


class PersonaCreate(PersonaBase):
    """Datos necesarios para crear una persona."""
    id: int


class PersonaUpdate(BaseModel):
    """Campos opcionales para actualizar una persona."""
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None


class Persona(PersonaBase):
    """Modelo que se devuelve en las respuestas."""
    id: int


# ==========================
# "BASE DE DATOS" EN MEMORIA
# ==========================

# En producción esto sería una tabla en la BD.
bd_personas: List[Persona] = []


# ==========================
# APLICACIÓN FASTAPI
# ==========================

app = FastAPI(title="CRUD de Personas", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción puedes restringir a tu dominio de Netlify
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ==========================
# ENDPOINTS (CRUD)
# ==========================

@app.get("/personas", response_model=List[Persona])
def listar_personas() -> List[Persona]:
    """Devuelve todas las personas."""
    return bd_personas


@app.get("/personas/{persona_id}", response_model=Persona)
def obtener_persona(persona_id: int) -> Persona:
    """Devuelve una persona por ID."""
    for persona in bd_personas:
        if persona.id == persona_id:
            return persona
    raise HTTPException(status_code=404, detail="Persona no encontrada")


@app.post("/personas", response_model=Persona, status_code=201)
def crear_persona(persona_crear: PersonaCreate) -> Persona:
    """Crea una nueva persona."""
    # Validar que el ID no exista
    for persona in bd_personas:
        if persona.id == persona_crear.id:
            raise HTTPException(status_code=400, detail="Ya existe una persona con ese ID")

    nueva_persona = Persona(**persona_crear.dict())
    bd_personas.append(nueva_persona)
    return nueva_persona


@app.put("/personas/{persona_id}", response_model=Persona)
def actualizar_persona(persona_id: int, datos_actualizacion: PersonaUpdate) -> Persona:
    """Actualiza parcialmente una persona por ID."""
    for idx, persona in enumerate(bd_personas):
        if persona.id == persona_id:
            datos = datos_actualizacion.dict(exclude_unset=True)
            persona_actualizada = persona.copy(update=datos)
            bd_personas[idx] = persona_actualizada
            return persona_actualizada

    raise HTTPException(status_code=404, detail="Persona no encontrada")


@app.delete("/personas/{persona_id}", status_code=204)
def eliminar_persona(persona_id: int) -> None:
    """Elimina una persona por ID."""
    for idx, persona in enumerate(bd_personas):
        if persona.id == persona_id:
            bd_personas.pop(idx)
            return

    raise HTTPException(status_code=404, detail="Persona no encontrada")
