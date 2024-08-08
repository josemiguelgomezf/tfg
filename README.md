# Desarrollo de herramienta de web-scraping potenciada por IA para la extracción automática de información estructurada de sitios web con diseño heterogéneo

Este repositorio contiene el código y los recursos utilizados en el Trabajo de Fin de Grado titulado **"Desarrollo de herramienta de web-scraping potenciada por IA para la extracción automática de información estructurada de sitios web con diseño heterogéneo"**. Este trabajo aborda un análisis detallado de las tecnologías de web scraping y su integración con inteligencia artificial, enfocándose en la extracción de información heterogénea de los consejos editoriales de revistas científicas.

## Estructura del Proyecto

El código principal del proyecto se encuentra en un archivo Python que realiza las siguientes tareas:

1. **Carga de Variables de Entorno:**
   - Utiliza la librería `dotenv` para cargar las variables de entorno, como la clave de API para OpenAI.

2. **Obtención de Datos Crudos mediante Web Scraping:**
   - Emplea la librería `requests` para realizar solicitudes HTTP y `BeautifulSoup` para extraer el contenido textual de las páginas web.
   - Filtra el contenido relevante eliminando etiquetas innecesarias (como `script` y `style`).

3. **División de Datos Crudos:**
   - Divide los datos extraídos en fragmentos más pequeños para manejarlos más fácilmente durante el procesamiento con GPT-3.5 Turbo.

4. **Extracción de Información Estructurada con GPT-3.5 Turbo:**
   - Utiliza el modelo de lenguaje de OpenAI para procesar los fragmentos de datos y extraer información estructurada, como los nombres, roles, universidades y países de los miembros del consejo editorial de las revistas científicas.

5. **Guardado de la Información en un Archivo JSON:**
   - La información estructurada se guarda en archivos JSON para facilitar su análisis posterior.

## Requisitos Previos

Antes de ejecutar el código, asegúrate de tener instaladas las siguientes dependencias:

- `requests`
- `beautifulsoup4`
- `openai`
- `python-dotenv`
  
Puedes instalar estas dependencias ejecutando:

pip install requests beautifulsoup4 openai python-dotenv
También necesitarás una clave de API de OpenAI, la cual debes configurar en un archivo .env:

OPENAI_API_KEY=tu_clave_de_api
Uso del Código
Clona este repositorio en tu máquina local.

Crea un archivo .env en el directorio raíz del proyecto y añade tu clave de API de OpenAI.

Ejecuta el script principal para iniciar el proceso de extracción:
El script recorrerá los sitios web especificados en la lista journals, extraerá los datos de los consejos editoriales y guardará la información estructurada en archivos JSON.

Estructura del Código
A continuación se presenta una descripción básica de las principales funciones y componentes del código:

get_raw_data_from_url(url): Realiza web scraping para obtener los datos crudos de una URL.
chunk_data(raw_data, chunk_size=10000): Divide los datos crudos en fragmentos manejables.
get_names_with_chatgpt(raw_data_chunks, journal_info): Utiliza GPT-3.5 Turbo para extraer nombres y otra información relevante del consejo editorial.
journals: Lista de revistas científicas con sus URLs, nombres, temas e ISSN.
Bucle principal: Itera sobre las revistas, ejecutando las funciones anteriores y guardando los resultados en archivos JSON.
Ejemplo de Uso
Al ejecutar el script, se generarán archivos JSON con la información del consejo editorial para cada revista especificada. Por ejemplo:

[
    {
        "nombre": "Felix Chan",
        "rol": "Editor in Chief",
        "universidad": "Universidad de California",
        "pais": "USA",
        "revista": "Nature Machine Intelligence",
        "tema": "Inteligencia Artificial",
        "issn": "2522-5839"
    },
    ...
]
Contacto
Este trabajo fue desarrollado en la Universidad de Alcalá, en la Escuela Politécnica Superior. Para más información, puedes contactar con el autor del proyecto.
