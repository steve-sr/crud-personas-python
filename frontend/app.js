
const API_BASE_URL = "https://crud-personas-python.onrender.com";

const tablaPersonas = document.getElementById("tabla-personas");
const formPersona = document.getElementById("form-persona");

async function obtenerPersonas() {
  const respuesta = await fetch(`${API_BASE_URL}/personas`);
  if (!respuesta.ok) {
    console.error("Error al obtener personas");
    return;
  }
  const personas = await respuesta.json();
  renderizarTabla(personas);
}

function renderizarTabla(personas) {
  tablaPersonas.innerHTML = "";

  if (personas.length === 0) {
    const fila = document.createElement("tr");
    const celda = document.createElement("td");
    celda.colSpan = 5;
    celda.textContent = "No hay personas registradas.";
    fila.appendChild(celda);
    tablaPersonas.appendChild(fila);
    return;
  }

  personas.forEach((p) => {
    const fila = document.createElement("tr");

    const celdaId = document.createElement("td");
    celdaId.textContent = p.id;

    const celdaNombre = document.createElement("td");
    celdaNombre.textContent = p.nombre;

    const celdaApellido = document.createElement("td");
    celdaApellido.textContent = p.apellido;

    const celdaEmail = document.createElement("td");
    celdaEmail.textContent = p.email || "sin email";

    const celdaAcciones = document.createElement("td");
    celdaAcciones.classList.add("actions");

    const botonEditar = document.createElement("button");
    botonEditar.textContent = "Editar";
    botonEditar.addEventListener("click", () => {
      cargarEnFormulario(p);
    });

    const botonEliminar = document.createElement("button");
    botonEliminar.textContent = "Eliminar";
    botonEliminar.addEventListener("click", async () => {
      await eliminarPersona(p.id);
    });

    celdaAcciones.appendChild(botonEditar);
    celdaAcciones.appendChild(botonEliminar);

    fila.appendChild(celdaId);
    fila.appendChild(celdaNombre);
    fila.appendChild(celdaApellido);
    fila.appendChild(celdaEmail);
    fila.appendChild(celdaAcciones);

    tablaPersonas.appendChild(fila);
  });
}

function cargarEnFormulario(persona) {
  document.getElementById("id").value = persona.id;
  document.getElementById("nombre").value = persona.nombre;
  document.getElementById("apellido").value = persona.apellido;
  document.getElementById("email").value = persona.email || "";

  // Evitar que cambien el ID y el email al editar
  document.getElementById("id").readOnly = true;
  document.getElementById("email").readOnly = true;

  const btn = document.getElementById("btn-submit");
  btn.textContent = "Actualizar";
  btn.classList.add("update-mode");
}


formPersona.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const id = Number(document.getElementById("id").value);
  const nombre = document.getElementById("nombre").value.trim();
  const apellido = document.getElementById("apellido").value.trim();
  const emailValue = document.getElementById("email").value.trim();
  const email = emailValue === "" ? null : emailValue;

  const persona = { id, nombre, apellido, email };

  // Verificamos si la persona ya existe para decidir POST o PUT
  const respuestaExiste = await fetch(`${API_BASE_URL}/personas/${id}`);

  if (respuestaExiste.ok) {
    // Existe: ACTUALIZAR SOLO nombre y apellido
    await fetch(`${API_BASE_URL}/personas/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, apellido }), // 👈 solo esto
    });
  } else {
    // No existe: CREAR con id, nombre, apellido, email
    await fetch(`${API_BASE_URL}/personas`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(persona),
    });
  }

  formPersona.reset();
  document.getElementById("id").readOnly = false;
  document.getElementById("email").readOnly = false;

  await obtenerPersonas();
});


async function eliminarPersona(id) {
  const confirmar = window.confirm("¿Seguro que quieres eliminar esta persona?");
  if (!confirmar) return;

  const respuesta = await fetch(`${API_BASE_URL}/personas/${id}`, {
    method: "DELETE",
  });

  if (!respuesta.ok) {
    console.error("Error al eliminar persona");
  }

  await obtenerPersonas();
}

// Cargar datos al inicio
obtenerPersonas();
