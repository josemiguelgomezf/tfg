import requests
from bs4 import BeautifulSoup
import json
import re

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

        # Recorrer los elementos y extraer la información de cada editor
        editors_info = []
        for element in editor_elements:
            # Filtrar los elementos que podrían contener información de editores
            if 'editor' in element.get_text().lower():  # Buscar la palabra 'editor' en el contenido del elemento
                editor_info = {
                    "editor": element.get_text().strip(),
                    "orcid": extract_orcid(element),
                    "affiliation": extract_affiliation(element),
                    "role": extract_role(element),
                    "journal": extract_journal(soup),
                    "publisher": extract_publisher(soup),
                    "issn": extract_issn(soup),
                    "date": extract_date(soup),
                    "url": url  # URL de la revista
                }
                editors_info.append(editor_info)

        return editors_info

    except requests.RequestException as e:
        print("Error de conexión:", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def extract_orcid(element):
    # Extraer el ORCID si está presente en el contenido del elemento
    orcid_pattern = re.compile(r'ORCID:\s*(\d{4}-\d{4}-\d{4}-\d{3}[\dX])', re.IGNORECASE)
    match = orcid_pattern.search(element.get_text())
    if match:
        return match.group(1)
    else:
        return ""

def extract_affiliation(element):
    # Extraer la afiliación si está presente en el contenido del elemento
    # Buscamos elementos con la clase 'affiliation' dentro del elemento actual
    affiliation = element.find(class_='affiliation')
    if affiliation:
        return affiliation.get_text().strip()
    else:
        return ""

def extract_role(element):
    # Extraer el rol si está presente en el contenido del elemento
    # Buscamos elementos con la clase 'role' dentro del elemento actual
    role = element.find(class_='role')
    if role:
        return role.get_text().strip()
    else:
        return ""

def extract_journal(soup):
    # Extraer el nombre de la revista de la página web
    # Intentamos encontrar un elemento que contenga el nombre de la revista
    journal_element = soup.find(class_='journal-name')
    if journal_element:
        return journal_element.get_text().strip()
    else:
        return ""

def extract_publisher(soup):
    # Extraer el nombre del editor/publisher de la página web
    # Intentamos encontrar un elemento que contenga el nombre del editor/publisher
    publisher_element = soup.find(class_='publisher-name')
    if publisher_element:
        return publisher_element.get_text().strip()
    else:
        return ""

def extract_issn(soup):
    # Extraer el ISSN de la página web
    # Intentamos encontrar un elemento que contenga el ISSN
    issn_element = soup.find('p', text=re.compile(r'ISSN'))
    if issn_element:
        return re.search(r'ISSN:\s*([\d\-]+)', issn_element.get_text()).group(1)
    else:
        return ""

def extract_date(soup):
    # Extraer la fecha de publicación de la página web
    # Intentamos encontrar un elemento que contenga la fecha de publicación
    date_element = soup.find('p', class_='publication-date')
    if date_element:
        return date_element.get_text().strip()
    else:
        return ""

# URL de la página web que contiene la información de los editores
website = "https://link.springer.com/journal/500/editors"

# Encontrar la información de los editores
editor_info = find_editor_info(website)

# Guardar la información de los editores en un archivo JSON
if editor_info:
    with open("editor_info.json", "w") as f:
        json.dump(editor_info, f, indent=4)
    print("La información de los editores se ha guardado en 'editor_info.json'.")
else:
    print("No se pudo encontrar información de los editores.")
