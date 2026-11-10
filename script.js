
// SELECCIONAR PAQUETE TURÍSTICO
document.querySelectorAll(".reservar").forEach(boton => {

    boton.addEventListener("click", () => {

        const paquete = boton.dataset.paquete;

        document.getElementById("paquete").value = paquete;

        document.getElementById("contacto")
            ?.scrollIntoView({ behavior: "smooth" });

        document.getElementById("contacto") ||
            document.getElementById("formCotizacion")
                .scrollIntoView({ behavior: "smooth" });
    });

});

// FECHA MÍNIMA: HOY
const fechaInput = document.getElementById("fecha");

const hoy = new Date();

const fechaLocal = new Date(
    hoy.getTime() - hoy.getTimezoneOffset() * 60000
).toISOString().split("T")[0];

fechaInput.min = fechaLocal;


// ENVIAR FORMULARIO AL BACKEND PYTHON
const formulario = document.getElementById("formCotizacion");

formulario.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const boton = document.getElementById("btnEnviar");
    const mensaje = document.getElementById("mensaje");

    const datos = {
        nombre: document.getElementById("nombre").value.trim(),
        correo: document.getElementById("correo").value.trim(),
        paquete: document.getElementById("paquete").value,
        personas: Number(document.getElementById("personas").value),
        fecha: document.getElementById("fecha").value,
        comentarios: document.getElementById("comentarios").value.trim()
    };

    boton.disabled = true;
    boton.textContent = "Enviando...";
    mensaje.textContent = "";

    try {

        const respuesta = await fetch("/api/cotizaciones", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(datos)

        });

        const resultado = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(resultado.error || "No se pudo enviar la solicitud.");
        }

        mensaje.textContent =
            "¡Solicitud registrada correctamente! Gracias por elegir Colca Trek. Código: " +
            resultado.id;

        mensaje.style.color = "#187345";

        formulario.reset();

    } catch (error) {

        mensaje.textContent = error.message;
        mensaje.style.color = "#c0392b";

    } finally {

        boton.disabled = false;
        boton.textContent = "Enviar cotización";

    }

});
