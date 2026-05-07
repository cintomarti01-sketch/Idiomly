import os
#import google.generativeai as genai
import random
import json # Importem la llibreria per fer JSON

# ---------- TRIAR PAÍS -----------
with open("paisos_europa_idiomes.txt", "r", encoding="utf-8") as f:
    content = f.readlines()

# Triem una línia aleatòria (evitem l'error del comptador manual)
linia_aleatoria = random.choice(content)
pais_data = linia_aleatoria.strip().split(',')
nom_pais = pais_data[0]
idioma = pais_data[1]

# ---------- GENERAR FRASE -----------
#clau_api = "LA_TEVA_CLAU_API_AQUI"
#genai.configure(api_key=clau_api)
#model = genai.GenerativeModel('gemini-1.5-flash')

# Demanem a la IA que ens doni la frase original i la traducció
prompt = f"Genera una frase en {idioma} d'ús col·loquial a {nom_pais} (5-10 paraules). També la seva traducció al català. Respon només en format JSON: {{\"original\": \"...\", \"catala\": \"...\"}}"


#resposta = model.generate_content(prompt)
resposta = {"original": "In bocca al lupo per tutto quanto!", "catala": "Molta sort amb tot plegat!"}
#dades_frase = json.loads(resposta.text) # Convertim el text de la IA a diccionari Python
dades_frase = resposta

# Afegim el país a les dades que guardarem (per comprovar després si l'usuari encerta)
dades_frase['pais_correcte'] = nom_pais

# Guardem el resultat en un fitxer JSON
with open("dades_joc.json", "w", encoding="utf-8") as f_json:
    json.dump(dades_frase, f_json, ensure_ascii=False, indent=4)

print("Joc del dia generat correctament!")
