  // Esperar a que el documento se cargue completamente
  document.addEventListener("DOMContentLoaded", function () {
    // Obtener la referencia al elemento <input>
    var inputElement = document.getElementsByClassName("input");

    // Verificar si el elemento tiene el atributo "hx-trigger"
    if (inputElement.hasAttribute("hx-trigger")) {
      // Asignar el valor "Hola mundo" al atributo "hx-trigger"
      inputElement.setAttribute("hx-trigger", "keyup changed delay:300ms");
      console.log("Se modificó el atributo hx-trigger.");
    } else {
      console.log("El atributo hx-trigger no está presente en el elemento.");
    }
  });