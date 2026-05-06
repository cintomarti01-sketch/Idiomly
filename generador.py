import os
import google.generativeai as genai
import random

# ---------- TRIAR PAÍS -----------

counter = 0

f = open("paisos_europa_idiomes.txt", "r")

content = f.readlines()

n = random.randint(1, counter)

pais = content[n].split(',')

f.close()

# ---------- GENERAR FRASE -----------

clau_api = "LA_TEVA_CLAU_API_AQUI"
genai.configure(api_key=clau_api)

model = genai.GenerativeModel('gemini-1.5-flash')

prompt = f"Genera una frase en {pais[1]}. Ha de ser una frase d'entre 5 i 10 paraules. La frase ha de ser una frase d'us col·loquial usada en {pais[0]}.

frase = model.generate_content(prompt)
