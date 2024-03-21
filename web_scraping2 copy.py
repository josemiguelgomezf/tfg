import requests
from bs4 import BeautifulSoup

def find_editor_info(url):
    try:
        # Realizar la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()  # Generar una excepción en caso de error HTTP
        content = response.text

        # Analizar el contenido HTML
        soup = BeautifulSoup(content, 'html.parser')

        # Encontrar todos los elementos que podrían contener información de editores
        editor_elements = soup.find_all(['p', 'div', 'span'], class_=True)

        # Recorrer los elementos y extraer la información
        editors_info = []
        for element in editor_elements:
            # Filtrar los elementos que podrían contener información de editores
            if 'editor' in element.get_text().lower():  # Buscar la palabra 'editor' en el contenido del elemento
                editors_info.append(element.get_text().strip())

        return editors_info

    except requests.RequestException as e:
        print("Error de conexión:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

# URL de la página web que contiene la información de los editores
website = "https://link.springer.com/journal/500/editors"

# Encontrar la información de los editores
editor_info = find_editor_info(website)

# Imprimir la información de los editores
if editor_info:
    print("Información de los editores encontrada:")
    for info in editor_info:
        print(info)
else:
    print("No se pudo encontrar información de los editores.")
