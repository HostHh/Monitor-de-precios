import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
TOTAL_PAGINAS = 3
ARCHIVO_HISTORIAL = "price_history.csv"

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
        precio = articulo.find("p", class_="price_color").text.replace("£", "")
        libros.append({
            "titulo": titulo,
            "precio": precio,
            "fecha": ahora
        })
    return libros

def main():
    todos_los_libros = []
    for pagina in range(1, TOTAL_PAGINAS + 1):
        print(f"Extrayendo página {pagina}/{TOTAL_PAGINAS}...")
        todos_los_libros.extend(obtener_libros_de_pagina(pagina))

    # La diferencia clave: si el archivo ya existe, AGREGAMOS filas
    # nuevas al final en vez de borrar lo que ya había. Así, cada vez
    # que corres el script, se suma un nuevo "snapshot" con fecha,
    # y con el tiempo se arma un historial real de precios.
    archivo_existe = os.path.isfile(ARCHIVO_HISTORIAL)

    with open(ARCHIVO_HISTORIAL, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["titulo", "precio", "fecha"])
        if not archivo_existe:
            escritor.writeheader()  # solo escribe encabezados la primera vez
        escritor.writerows(todos_los_libros)

    print(f"\nListo. Se agregaron {len(todos_los_libros)} registros a {ARCHIVO_HISTORIAL}")
    print("Corre este script varios días seguidos para construir historial real.")
    print("Luego sube ese archivo .csv al dashboard para ver las gráficas.")

if __name__ == "__main__":
    main()
