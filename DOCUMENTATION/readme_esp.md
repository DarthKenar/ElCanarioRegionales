[Volver][volver]

![Logo ElCanarioRegionales](../docs/images/logo-header.png)

# Objetivo

> Aplicación web para control de Stock, Clientes y Ordenes para un pequeño negocio.

## Primeros pasos

## Con python instalado

[Download Python](https://www.python.org/downloads/release/python-3120/)

### Clonar proyecto

```bash
git clone https://github.com/DarthKenar/ElCanarioRegionales.git
```

#### Instala mkdocs para visualizar la documentacion completa del proyecto

```bash
pip install mkdocs
```

#### En el directorio actual del proyecto ejecuta

```bash
mkdocs serve
```

![MKDOCS](../docs/images/mkdocs.png)

---

#### > Para ejecutar la aplicacion con PDM

##### Si no tienes pdm (instálalo)

```bash
pip install pdm
```

##### Si tienes pdm o una vez que lo tengas

#### Instala las dependencias en el entorno virtual con

```bash
pdm install
```
#### Realiza las migraciones para utilizar una base de datos local con

```bash
pdm migrate
```

#### Ejecuta el servidor con

```bash
pdm server
```

---

#### > Para ejecutar la aplicacion con PIP

```bash
py -m venv nombre_del_entorno
```

#### Activa el entorno virtual

```bash
source nombre_del_entorno/bin/activate
```

#### En el entorno virtual activado

```bash
pip install -r requirements.txt
```

#### Con las dependencias ya instaladas nos dirigimos a la carpeta que contiene el archivo python manage

```bash
cd ElCanarioRegionales
cd elCanario
```

#### Comprobamos que en el directorio se encuentre el archivo python manage

```bash
cd dir
```

![List directory](../docs/images/path.png)

#### Realizamos las migraciones para tener una base de datos local

```bash
py manage.py migrate
```

---

## PREVIEW

[Volver][volver]

[volver]: /README.md
