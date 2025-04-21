
document.addEventListener("DOMContentLoaded", function() {
    fetch('https://s8ahp7qrhg.execute-api.us-east-1.amazonaws.com/Prod/getVisitorCount')
        .then(response => response.json())
        .then(data => {
            console.log("Valor de visitas:", data.count);
            const visitorCountElement = document.getElementById('visitorCount');
            visitorCountElement.textContent = data.count;
            visitorCountElement.style.color = "#ff0000";
        })
        .catch(error => {
            console.error('Error al obtener el contador de visitas:', error);
            const visitorCountElement = document.getElementById('visitorCount');
            visitorCountElement.textContent = "Error";
            visitorCountElement.style.color = "#ff0000";
        });
});
