import re
from colorama import Fore
import requests

website = "https://www.nature.com/natmachintell/editors"
resultado = requests.get(website)
content = resultado.text
#print(content)

patron = r": [\w-]*"
repeated_editors = re.findall(patron, str(content))
editors = list(set(repeated_editors))

editors_final = []

for i in editors:
    editors = i.replace("/entry/", "")
    editors_final.append(editors)
    print(editors)

print(repeated_editors)
###########################

#maquina_noob = "noob-1"
#existe_noob = False

#for a in maquinas_final:
#    if a == maquina_noob:
#        existe_noob = True
#        break

#color_verde = Fore.GREEN
#color_amarillo = Fore.YELLOW

#if existe_noob == True:
#    print("\n" + color_verde + "No hay ninguna máquina nueva")
#else:
#    print("\n" + color_amarillo + "Máquina nueva!!!!")