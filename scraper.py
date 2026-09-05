import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGINAS = 3
ARCHIVO_HISTORIAL = "price_history.json"

def obtener_libros_de_pagina(numero_pagina):
    url = BASE_URL.format(numero_pagina)
    respuesta = requests.get(url)

    if respuesta.status_code != 200:
        print(f"  Aviso: página {numero_pagina} devolvió estado {respuesta.status_code}")
        return []

    soup = BeautifulSoup(respuesta.text, "html.parser")
    articulos = soup.find_all("article", class_="product_pod")

    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    libros = []
    for articulo in articulos:
        titulo = articulo.find("h3").find("a")["title"]
      precio_texto = articulo.find("p", class_="price_color").text
precio = float(''.join(c for c in precio_texto if c.isdigit() or c == '.'))
        libros.append({"titulo": titulo, "precio": precio, "fecha": ahora})
    return libros

def cargar_historial_existente():
    if os.path.isfile(ARCHIVO_HISTORIAL):
        with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    return []

def main():
    historial = cargar_historial_existente()

    nuevos_registros = []
    for pagina in range(1, TOTAL_PAGINAS + 1):
        print(f"Extrayendo página {pagina}/{TOTAL_PAGINAS}...")
        nuevos_registros.extend(obtener_libros_de_pagina(pagina))

    historial.extend(nuevos_registros)

    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as archivo:
        json.dump(historial, archivo, ensure_ascii=False, indent=2)

    print(f"\nListo. El historial ahora tiene {len(historial)} registros en total.")

if __name__ == "__main__":
    main()
