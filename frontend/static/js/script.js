document.getElementById("loginForm").addEventListener("submit", async function(event) {

    // Evitar que la página se recargue
    event.preventDefault();

    // Obtener datos
    const usuario = document.getElementById("usuario").value;
    const password = document.getElementById("password").value;

    const mensaje = document.getElementById("mensaje");

    try {

        // Enviar datos a FastAPI
        const respuesta = await fetch(
            "http://192.168.0.251:8000/usuarios/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    usuario: usuario,
                    password: password
                })
            }
        );

        const datos = await respuesta.json();

        // LOGIN CORRECTO
        if (respuesta.ok) {

            // Guardar información
            localStorage.setItem(
                "access_token",
                datos.access_token
            );

            localStorage.setItem(
                "usuario",
                datos.usuario
            );

            localStorage.setItem(
                "rol",
                datos.rol
            );

            localStorage.setItem(
                "personal_id",
                datos.personal_id
            );

            mensaje.textContent = "Inicio de sesión correcto";

            // ==========================================
            // REDIRECCIÓN SEGÚN EL ROL
            // ==========================================

            if (datos.rol === "Admin") {

                window.location.href = "/admin";

            } else if (datos.rol === "Doctor") {

                window.location.href = "/doctor";

            } else if (datos.rol === "Enfermero") {

                window.location.href = "/enfermero";

            } else {

                mensaje.textContent =
                    "El usuario tiene un rol no válido.";
            }

        } else {

            // LOGIN INCORRECTO
            mensaje.textContent = datos.detail;

        }

    } catch (error) {

        console.error(error);

        mensaje.textContent =
            "No se pudo conectar con el servidor";

    }

});