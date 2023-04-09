# ⏬ imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
import json


Provincias = {}

with open('C:\\Users\\Usuario\\source\\SB\\SubastasBOE\\urls.json', encoding='utf-8') as f:
    data = json.load(f)
    for key, val in data.items():
        Provincias[key] = val.strip()

for provincia, url in Provincias.items():
    print(f"Provincia: {provincia}, URL: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

# 🥣 requests y sopa

soup = BeautifulSoup(response.content, 'html.parser')
results = soup.find_all('li', {'class':'resultado-busqueda'})

# 📝preparando listas vacias
titulo = []
donde = []
expediente = []
link = []
descripcion = []

# 🔁 list iterations
rango = [1]
for i in rango:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('li', {'class':'resultado-busqueda'})
for result in results:
    titulo.append(result.find('h3').get_text().strip().replace('\n', ''))
    donde.append(result.find('h4').get_text().replace('1Ẃ', 'de 1a').strip())
    expediente.append(result.find('p').get_text().strip())
    descripcion.append(result.findNext('p').get_text().strip())
    link.append(result.find('a', {'class' : 'resultado-busqueda-link-defecto'}).get('href'))


# 📊 creando dataframe y retoques
subastas = pd.DataFrame({'titulo': titulo, 'donde': donde, 'expediente': expediente, 'descripcion': descripcion, 'link': link})
subastas['link'] = subastas['link'].apply(lambda x: f"{url}/{x}")

print(subastas)

# 🐱‍💻 pal saco
subastas.to_csv('subastas.csv', index=False)

