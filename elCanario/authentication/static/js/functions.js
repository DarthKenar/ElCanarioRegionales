var miBoton = document.getElementById("cambiarTexto");

// Función para verificar el tamaño de la pantalla y cambiar el texto del botón
function cambiarTextoBoton() {
    if (window.innerWidth >= 768) { // Cambiar 768 al ancho deseado para "pantalla grande"
        miBoton.value = "Pantalla Grande";
    } else {
        miBoton.value = "Pantalla Chica";
    }
}

// Llama a la función inicialmente y cada vez que cambie el tamaño de la ventana
cambiarTextoBoton();
window.addEventListener("resize", cambiarTextoBoton);