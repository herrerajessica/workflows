console.log("counter-v2.js cargado correctamente");

document.addEventListener("DOMContentLoaded", function () {
  fetch("https://s8ahp7qrhg.execute-api.us-east-1.amazonaws.com/Prod/getVisitorCount")
    .then(response => response.json())
    .then(data => {
      console.log("Respuesta completa de la API con sam:", data);

      const count = data.count; // aquí el cambio real
      console.log("Valor de visitas:", count);

      const visitorCountElement = document.getElementById('visitorCount');
      visitorCountElement.textContent = count ?? "N/A";
      visitorCountElement.style.color = "#ff0000";
    })
    .catch(error => {
      console.error('Error al obtener el contador de visitas:', error);
      const visitorCountElement = document.getElementById('visitorCount');
      visitorCountElement.textContent = "Error";
      visitorCountElement.style.color = "#ff0000";
    });
});
