import re
import requests
from bs4 import BeautifulSoup
import spacy

# Cargar el modelo de lenguaje de SpaCy con el componente NER
# python -m spacy download es_core_news_md
nlp = spacy.load("es_core_news_md")

#Se necesita instalar la biblioteca lxml

website = "https://www.nature.com/natmachintell/editors"

content = requests.get(website).text

soup = BeautifulSoup(content, 'lxml')
#Funcion prettify se utiliza para darle formato al html
#print(soup.prettify())

#Funcion para buscar esta tambien find_all
editors_html = soup.find_all('p')
#Recorremos unn bucle la busqueda que hemos realizado
#for editor in editors_html:
#    print(editor.text)

#Funcion para buscar un editor
def buscar_editor(parrafo):
    # Definimos un patrón de expresión regular que busca las palabras específicas en el párrafo
    patron = re.compile(r'\b(Chief Editor|Senior Editor|Associate Editor)\b', re.IGNORECASE)
    # Buscamos todas las coincidencias en el párrafo
    coincidencias = patron.findall(parrafo)
    # Si encontramos alguna coincidencia, devolvemos True, de lo contrario, devolvemos False
    return bool(coincidencias)

def es_nombre(texto):
    doc = nlp(texto)
    for entidad in doc.ents:
        if entidad.label_ == "PER":  # PER es la etiqueta para nombres de personas
            return True
    return False

#Funcion para buscar un editor
def buscar_email(parrafo):
    # Definimos un patrón de expresión regular que busca las palabras específicas en el párrafo
    patron = re.compile(r'\b(@|@.com)\b', re.IGNORECASE)
    # Buscamos todas las coincidencias en el párrafo
    coincidencias = patron.findall(parrafo)
    # Si encontramos alguna coincidencia, devolvemos True, de lo contrario, devolvemos False
    return bool(coincidencias)

def extraer_email(parrafo):
    # Definimos un patrón de expresión regular para encontrar direcciones de correo electrónico
    patron = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    # Buscamos todas las coincidencias en el párrafo
    coincidencias = patron.findall(parrafo)
    # Devolvemos la primera coincidencia encontrada
    if coincidencias:
        return coincidencias[0]
    else:
        return None

def extraer_editores(parrafo):
    # Definimos un patrón de expresión regular que busca las palabras específicas en el párrafo
    patron = re.compile(r'\b(Chief Editor|Senior Editor|Associate Editor)\b', re.IGNORECASE)
    # Buscamos todas las coincidencias en el párrafo
    coincidencias = patron.findall(parrafo)
    # Devolvemos la lista de todas las coincidencias encontradas
    return coincidencias[0]

def extraer_nombre_editor(parrafo):
    # Definimos un patrón de expresión regular que busca nombres y apellidos de editor
    patron = re.compile(r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b')
    # Buscamos todas las coincidencias en el párrafo
    coincidencias = patron.findall(parrafo)
    nombres = ''
    for coincidencia in coincidencias:
        for coincidencia_detalle in coincidencia:
            if es_nombre(coincidencia_detalle):
                nombres=nombres+coincidencia_detalle+' '
    # Devolvemos la lista de nombres y apellidos encontrados
    return nombres

#Funcion para buscar esta tambien find_all
parrafos_html = soup.find_all('p')
#Recorremos unn bucle la busqueda que hemos realizado
for parrafo in parrafos_html:
    if buscar_editor(parrafo.text):
        print(extraer_editores(parrafo.text))
        print(extraer_nombre_editor(parrafo.text))

    if buscar_email(parrafo.text):
        print(extraer_email(parrafo.text))

