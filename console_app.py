from dataclasses import dataclass
from typing import List, Optional


# ==========================
# MODELO
# ==========================

@dataclass
class Persona:
    """Modelo simple de persona."""
    id: int
    nombre: str
    apellido: str
    email: Optional[str] = None


# ==========================
# LÓGICA DE NEGOCIO (CRUD)
# ==========================

def crear_persona(personas: List[Persona], persona: Persona) -> None:
    """Agrega una nueva persona a la lista."""
    personas.append(persona)


def listar_personas(personas: List[Persona]) -> None:
    """Imprime la lista de personas."""
    if not personas:
        print("\nNo hay personas registradas todavía.")
        return

    print("\nListado de personas:")
    for p in personas:
        email = p.email if p.email is not None else "sin email"
        print(f"- [{p.id}] {p.nombre} {p.apellido} ({email})")


def buscar_persona_por_id(personas: List[Persona], persona_id: int) -> Optional[Persona]:
    """Devuelve la persona con ese ID, o None si no existe."""
    for p in personas:
        if p.id == persona_id:
            return p
    return None


def actualizar_persona(
    personas: List[Persona],
    persona_id: int,
    nuevo_nombre: Optional[str] = None,
    nuevo_apellido: Optional[str] = None,
    nuevo_email: Optional[str] = None,
) -> bool:
    """
    Actualiza una persona.
    Devuelve True si se actualizó, False si no se encontró.
    """
    persona = buscar_persona_por_id(personas, persona_id)
    if persona is None:
        return False

    if nuevo_nombre:
        persona.nombre = nuevo_nombre
    if nuevo_apellido:
        persona.apellido = nuevo_apellido
    # aquí sí puede ser cadena vacía para "borrar" el email
    if nuevo_email is not None:
        persona.email = nuevo_email or None

    return True


def eliminar_persona(personas: List[Persona], persona_id: int) -> bool:
    """
    Elimina una persona por ID.
    Devuelve True si se eliminó, False si no se encontró.
    """
    persona = buscar_persona_por_id(personas, persona_id)
    if persona is None:
        return False

    personas.remove(persona)
    return True


# ==========================
# CAPA DE INTERFAZ (CONSOLa)
# ==========================

def mostrar_menu() -> None:
    """Muestra las opciones del menú principal."""
    print("\n=== CRUD de Personas ===")
    print("1) Crear persona")
    print("2) Listar personas")
    print("3) Actualizar persona")
    print("4) Eliminar persona")
    print("5) Salir")


def leer_entero(mensaje: str) -> int:
    """Lee un entero desde teclado, validando la entrada."""
    while True:
        valor = input(mensaje)
        if valor.isdigit():
            return int(valor)
        print("⚠️  Por favor, ingresa un número válido.")


def leer_texto_opcional(mensaje: str) -> Optional[str]:
    """
    Lee texto desde teclado.
    Si el usuario deja vacío, devuelve None.
    """
    valor = input(mensaje).strip()
    return valor or None


def main() -> None:
    """Punto de entrada del programa."""
    personas: List[Persona] = []

    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-5): ").strip()

        if opcion == "1":
            print("\n>>> Crear persona")
            persona_id = leer_entero("ID (número): ")
            if buscar_persona_por_id(personas, persona_id) is not None:
                print("⚠️  Ya existe una persona con ese ID.")
                continue

            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = leer_texto_opcional("Email (opcional, ENTER para omitir): ")

            nueva_persona = Persona(
                id=persona_id,
                nombre=nombre,
                apellido=apellido,
                email=email,
            )
            crear_persona(personas, nueva_persona)
            print("✅ Persona creada correctamente.")

        elif opcion == "2":
            listar_personas(personas)

        elif opcion == "3":
            print("\n>>> Actualizar persona")
            persona_id = leer_entero("ID de la persona a actualizar: ")
            persona = buscar_persona_por_id(personas, persona_id)
            if persona is None:
                print("⚠️  No existe una persona con ese ID.")
                continue

            print(f"Editando a: {persona.nombre} {persona.apellido}")
            print("Deja el campo vacío si no quieres cambiarlo.")
            nuevo_nombre = leer_texto_opcional("Nuevo nombre: ")
            nuevo_apellido = leer_texto_opcional("Nuevo apellido: ")
            print("Si quieres borrar el email, escribe un espacio y ENTER.")
            nuevo_email_raw = input("Nuevo email (ENTER para mantener): ").strip()
            # diferenciamos entre mantener, borrar y cambiar
            if nuevo_email_raw == "":
                nuevo_email = None  # mantener
            elif nuevo_email_raw == " ":
                nuevo_email = ""    # borrar -> se convertirá en None en la función
            else:
                nuevo_email = nuevo_email_raw

            actualizado = actualizar_persona(
                personas,
                persona_id,
                nuevo_nombre=nuevo_nombre,
                nuevo_apellido=nuevo_apellido,
                nuevo_email=nuevo_email,
            )
            if actualizado:
                print("✅ Persona actualizada.")
            else:
                print("⚠️  No se pudo actualizar (no encontrada).")

        elif opcion == "4":
            print("\n>>> Eliminar persona")
            persona_id = leer_entero("ID de la persona a eliminar: ")
            eliminado = eliminar_persona(personas, persona_id)
            if eliminado:
                print("✅ Persona eliminada.")
            else:
                print("⚠️  No existe una persona con ese ID.")

        elif opcion == "5":
            print("Saliendo del programa. ¡Hasta luego! 👋")
            break

        else:
            print("⚠️  Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
