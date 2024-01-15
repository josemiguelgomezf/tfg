import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Definir la información de la persona en la revista científica
persona_info = {
    "editor": "Nombre del Editor",
    "orcid": "ORCID de la persona",
    "affiliation": "Afiliación de la persona",
    "role": "Rol en la revista",
    "journal": "Nombre de la revista",
    "publisher": "Nombre del editor/publisher",
    "issn": "Número ISSN",
    "date": "Fecha de publicación",
    "url": "URL de la revista",
}

# Formatear la información en una cadena
user_message = f"I need a little text about {persona_info['role']} in {persona_info['journal']}."

# Imprimir el mensaje de usuario
print(user_message)

# Crear la instancia de OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Enviar el mensaje a OpenAI GPT-3.5 Turbo
chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": "The person's information is as follows:"},
    ],
    model="gpt-3.5-turbo"
)

# Obtener la respuesta de OpenAI
assistant_response = chat_completion.choices[0].message.content

# Imprimir la respuesta
print(assistant_response)

# Crear un archivo JSON con la estructura especificada
output_data = f"{persona_info['editor']},{persona_info['orcid']},{persona_info['affiliation']},{persona_info['role']},{persona_info['journal']},{persona_info['publisher']},{persona_info['issn']},{persona_info['date']},{persona_info['url']}"

# Guardar el archivo JSON
with open("output.json", "w") as file:
    file.write(output_data)

# Imprimir la ubicación del archivo guardado
print("Output JSON file saved as output.json")
