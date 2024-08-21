document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = window.location.origin + '/api';
    const resultadoDiv = document.getElementById('resultado');

    // Función para mostrar resultados
    function mostrarResultado(mensaje) {
        resultadoDiv.innerHTML = `<pre>${JSON.stringify(mensaje, null, 2)}</pre>`;
    }

    let authToken = '';

    async function hacerSolicitud(url, metodo, datos) {
        console.log(`Enviando solicitud ${metodo} a ${url}`);
        console.log('Datos:', datos);
        try {
            const response = await fetch(url, {
                method: metodo,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': authToken ? `Token ${authToken}` : ''
                },
                body: JSON.stringify(datos)
            });
            console.log('Respuesta recibida:', response);
            const data = await response.json();
            console.log('Datos recibidos:', data);
            return data;
        } catch (error) {
            console.error('Error en la solicitud:', error);
            throw error;
        }
    }

    // Registro
    document.getElementById('registroForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('regUsername').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;

        try {
            const data = await hacerSolicitud(`${apiUrl}/register/`, 'POST', { username, email, password });
            mostrarResultado(data);
        } catch (error) {
            console.error('Error completo:', error);
            mostrarResultado({ error: JSON.parse(error.message) });
        }
    });

    // Inicio de sesión
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const data = await hacerSolicitud(`${apiUrl}/login/`, 'POST', { email, password });
            if (data.token) {
                authToken = data.token;
                mostrarResultado({ message: 'Login exitoso', token: data.token });
            } else {
                mostrarResultado(data);
            }
        } catch (error) {
            mostrarResultado({ error: 'Error en el login' });
        }
    });

    // Página de inicio
    document.getElementById('homeBtn').addEventListener('click', async () => {
        try {
            const response = await fetch(`${apiUrl}/`, {
                method: 'GET',
            });
            const data = await response.json();
            mostrarResultado(data);
        } catch (error) {
            mostrarResultado({ error: 'Error al obtener el mensaje de bienvenida' });
        }
    });
});