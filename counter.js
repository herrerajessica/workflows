document.addEventListener("DOMContentLoaded", function() {
    fetch('https://mb77h5uai8.execute-api.us-east-1.amazonaws.com/getVisitorCount')
        .then(response => response.json())
        .then(data => {
            console.log("Valor de visitas:", data.visits); // Imprime el valor de visitas en la consola
            const visitorCountElement = document.getElementById('visitorCount');
            visitorCountElement.textContent = data.visits;
            visitorCountElement.style.color = "#ff0000";  // Cambia el color aquí
        })
        .catch(error => {
            console.error('Error al obtener el contador de visitas:', error);
            const visitorCountElement = document.getElementById('visitorCount');
            visitorCountElement.textContent = "Error";
            visitorCountElement.style.color = "#ff0000";  // Cambia el color en caso de error también
        });
});
