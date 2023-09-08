# Objetivos principales

- Mostrar los errores de un formulario a medida que se escribe
- solo guardar cuando se hace click en el botón guardar

## Entender como funciona UpdateView

    UpdateView simplifica la creación de vistas para la edición y actualización de registros de un modelo de Django. A continuación, se explican las principales características de UpdateView:

- Modelo (model)
  - La vista UpdateView espera que se le proporcione el modelo (base de datos) al que está asociada
- Formulario (form_class)
  - Puedes especificar un formulario personalizado que se utilizará para recopilar y validar los datos que se van a actualizar en el modelo
- Plantilla (template_name)
  - Puedes definir una plantilla personalizada que se utilizará para renderizar la página de edición de datos
- Método (POST)
  - En el método post, se realiza el procesamiento de los datos enviados a través de un formulario cuando se envía el formulario.
- URL de redirección exitosa (get_success_url)
  - Después de que se actualiza con éxito un registro, se necesita una URL a la que redirigir al usuario. El método get_success_url define esa URL
- Método form_valid y form_invalid
  - Estos métodos se llaman cuando el formulario es válido o inválido, respectivamente.

## Entender como funciona HTMX

    -   HTMX funciona mediante la incorporación de atributos especiales en elementos HTML, como botones o formularios. Estos atributos le indican a HTMX cómo debe comportarse la interacción en respuesta a eventos del usuario, como hacer clic en un botón o enviar un formulario. Cuando se produce un evento, HTMX se encarga de enviar una solicitud al servidor web (a menudo en segundo plano), obtener una respuesta del servidor y luego actualizar la parte específica de la página web con la nueva información, todo ello sin necesidad de recargar toda la página
