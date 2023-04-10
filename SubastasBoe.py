import os

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json


Provincias = {}

with open('C:\\Users\\Usuario\\Documents\\GitHub\\SubastasBOE\\urls.json', encoding='utf-8') as f:
    data = json.load(f)
    for key, val in data.items():
        Provincias[key] = val.strip()

# Create the "Provincias" directory if it doesn't exist
if not os.path.exists("Provincias"):
    os.mkdir("Provincias")

for provincia, url in Provincias.items():
    print(f"Provincia: {provincia}, URL: {url}")
    # Check if the URL has the correct domain prefix
    if not url.startswith("https://subastas.boe.es"):
        url = f"https://subastas.boe.es{url}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('li', {'class':'resultado-busqueda'})
    
    titulo = []
    donde = []
    expediente = []
    descripcion = []
    link = []
    datos_tabla = []

    for result in results:
        titulo.append(result.find('h3').get_text().strip().replace('\n', ''))
        donde.append(result.find('h4').get_text().replace('1Ş', 'de 1a').strip())
        expediente.append(result.find('p').get_text().strip())
        descripcion.append(result.findNext('p').get_text().strip())
        link.append(result.find('a', {'class' : 'resultado-busqueda-link-defecto'}).get('href'))

    for lnk in link:
        # Check if the link has the correct domain prefix
        if not lnk.startswith("https://subastas.boe.es"):
            lnk = f"https://subastas.boe.es{lnk}"
        link_response = requests.get(lnk)
        link_soup = BeautifulSoup(link_response.content, 'html.parser')

        try:
            datos_tabla.append(link_soup.find('div', {'id':'idBloqueDatos1'}).find('table'))
        except AttributeError:
            datos_tabla.append(None)

    subastas = pd.DataFrame({'titulo': titulo, 'donde': donde, 'expediente': expediente, 'descripcion': descripcion, 'link': link, 'datos_tabla': datos_tabla})
    subastas['link'] = subastas['link'].apply(lambda x: f"https://subastas.boe.es/{x}")

    # Save the CSV file inside the "Provincias" directory
    subastas.to_csv(os.path.join("Provincias", f"{provincia}.csv"), index=False)
    print(subastas)
