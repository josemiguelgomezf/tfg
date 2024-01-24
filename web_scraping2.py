import re
import requests
from bs4 import BeautifulSoup

#website = "https://www.nature.com/natmachintell/editors"
#Nature Machine Intelligence
website = "https://link.springer.com/journal/500/editors"
#SOFT COMPUTING

resultado = requests.get(website)
content = resultado.text

soup = BeautifulSoup(content, 'html.parser')

# Encuentra todos los elementos span con la clase 'bold-name'
#editors = soup.find_all('span', class_='bold-name')
#editors = soup.find_all('p')

# Imprime los nombres de los editores
#for editor in editors:
#    print(editor.text.strip())
# Encuentra todos los elementos span con la clase 'bold-name'
editors = soup.find_all('p')

# Patrones para extraer nombres, roles y correos electrónicos
pattern_name = re.compile(r'([A-Za-z]+ [A-Za-z]+),')
pattern_role = re.compile(r'([A-Za-z]+ Editor):')
pattern_email = re.compile(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')

# Listas para almacenar los resultados
matches_name = []
matches_role = []
matches_email = []

# Itera sobre los elementos de 'editors'
for editor in editors:
    # Extrae el texto de cada elemento
    editor_text = editor.get_text()
    print(editor_text)
    
    # Busca coincidencias en el texto
    match_name = re.search(pattern_name, editor_text)
    match_role = re.search(pattern_role, editor_text)
    match_email = re.search(pattern_email, editor_text)

    # Añade los resultados a las listas
    if match_name:
        matches_name.append(match_name.group(1).strip())
    if match_role:
        matches_role.append(match_role.group(1).strip())
    if match_email:
        matches_email.append(match_email.group(1).strip())

# Imprimir la información
for name, role, email in zip(matches_name, matches_role, matches_email):
    print(f"Nombre: {name}, Rol: {role}, Correo electrónico: {email}")
