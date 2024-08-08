import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
import json

# Carga de variables de entorno
load_dotenv()

# Función para obtener datos crudos de una URL mediante web scraping
def get_raw_data_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Eliminación de etiquetas innecesarias para reducir el tamaño del texto
        for tag in soup.find_all(['script', 'style']):
            tag.decompose()
        raw_data = soup.get_text(separator='\n', strip=True)
        return raw_data.encode("utf-8")
    else:
        print("Error al obtener datos de la URL:", response.status_code)
        return None

# Función para dividir los datos crudos en fragmentos más pequeños
def chunk_data(raw_data, chunk_size=10000):
    chunks = []
    for i in range(0, len(raw_data), chunk_size):
        chunks.append(raw_data[i:i + chunk_size])
    return chunks

# Función para obtener información estructurada del consejo editorial usando GPT-3.5 Turbo
def get_names_with_chatgpt(raw_data_chunks, journal_info):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    all_info = []
    try:
        # Iterar sobre los fragmentos de datos crudos
        for chunk in raw_data_chunks:
            text = chunk.decode("utf-8")
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": text},
                    {"role": "assistant", "content": "Por favor, proporciona una lista de miembros del consejo editorial con sus nombres, roles, universidades y países, separados por barras inclinadas (/), y cada persona separada por un punto y coma. No con saltos de línea. Recuerda que los editores pueden estar en la sección: Editorial Board, Co-Editors-in-Chief... Normalmente en la lista debe haber más de 5 personas. Céntrate en la EDITORIAL BOARD. Por ejemplo: Felix Chan/Editor in Chief/Universidad de California/USA, Jose Miguel Gomez/Associate Editor/Universidad de Alcala/España."},
                ],
                model="gpt-3.5-turbo",
                temperature=0.5,
            )
            assistant_response = chat_completion.choices[0].message.content
            print(assistant_response)
            names = assistant_response.split(";")
            # Crear diccionarios con información estructurada
            for name in names:
                name_parts = name.strip().split("/")
                if len(name_parts) >= 4:  # Asegurarse de tener al menos nombre, rol y país
                    person_info = {
                        "nombre": name_parts[0].strip(),
                        "rol": name_parts[1].strip(),
                        "universidad": name_parts[2].strip(),
                        "pais": name_parts[3].strip(),
                        "revista": journal_info[1],
                        "tema": journal_info[2],
                        "issn": journal_info[3]
                    }
                    all_info.append(person_info)
    except Exception as e:
        print("Error al procesar datos:", e)
    return all_info

# Información sobre el sitio web del consejo editorial y detalles de la revista
journals = [
    ["https://www.nature.com/natmachintell/editors", "Nature Machine Intelligence", "Inteligencia Artificial", "2522-5839"],
    ["https://www.cambridge.org/core/journals/knowledge-engineering-review/information/about-this-journal/editorial-board", "NETWORK-COMPUTATION IN NEURAL SYSTEMS", "COMPUTER SCIENCE", "0954-898X"]
]

# Bucle principal
for journal in journals:
    # Ruta del archivo JSON
    json_path = "editorial_names_" + journal[1] + ".json"
    # Leer el contenido existente del archivo JSON, si existe
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            existing_data = json.load(file)
    else:
        existing_data = []
    # Obtener datos crudos del sitio web
    raw_data = get_raw_data_from_url(journal[0])
    # Verificar si se obtuvieron datos crudos
    if raw_data:
        # Dividir datos crudos en fragmentos más pequeños
        raw_data_chunks = chunk_data(raw_data)
        # Obtener información estructurada del consejo editorial
        editorial_info = get_names_with_chatgpt(raw_data_chunks, journal)
        # Agregar nuevos datos al contenido existente
        existing_data.extend(editorial_info)
        # Guardar el contenido actualizado en el archivo JSON
        with open(json_path, "w") as file:
            json.dump(existing_data, file, indent=4)
        print("Información del consejo editorial para", journal[1], "guardada en", json_path)
    else:
        print("No se pudieron obtener datos crudos de la URL:", journal[0])
