import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time 

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Función para descargar la imagen de un jugador
def download_player_image(player_id):
    # Ruta donde se guardará la imagen
    image_path = f'data/images/{player_id}.jpg'

    # Verificar si la imagen ya existe
    if os.path.exists(image_path):
        print(f'La imagen de {player_id} ya existe. Omitiendo descarga.')
        return

    # Construir la URL de la página del jugador
    first_letter = player_id[0]  # Primera letra del ID
    url = f'https://www.pro-football-reference.com/players/{first_letter}/{player_id}.htm'

    # Hacer la solicitud HTTP
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza una excepción si el código de estado no es 200
    except requests.exceptions.HTTPError as e:
        print(f'Error: No se pudo acceder a la página de {player_id}. Código de estado: {response.status_code}')
        return
    except requests.exceptions.RequestException as e:
        print(f'Error: No se pudo conectar al servidor para {player_id}.')
        return

    # Parsear el contenido HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Buscar la imagen del jugador
    media_item = soup.find('div', class_='media-item')
    if not media_item:
        print(f'El jugador {player_id} no tiene imagen en su perfil.')
        return

    img_tag = media_item.find('img')
    if not img_tag:
        print(f'El jugador {player_id} no tiene imagen en su perfil.')
        return

    img_url = img_tag['src']
    if not img_url:
        print(f'El jugador {player_id} no tiene imagen en su perfil.')
        return

    # Descargar la imagen
    try:
        img_data = requests.get(img_url).content
    except requests.exceptions.RequestException as e:
        print(f'Error: No se pudo descargar la imagen de {player_id}.')
        return

    # Guardar la imagen localmente
    os.makedirs('data/images', exist_ok=True)  # Crear carpeta si no existe
    with open(image_path, 'wb') as f:
        f.write(img_data)

    print(f'Imagen de {player_id} descargada correctamente.')

qb_consolidated = pd.read_csv('data/processed/qb_stats.csv')

# Obtener los IDs únicos de los QB
unique_qb_ids = qb_consolidated['Player-additional'].unique()

# Iterar sobre cada ID único
for qb_id in reversed(unique_qb_ids):
    print(f'Procesando QB con ID: {qb_id}')
    # Aquí puedes llamar a la función download_player_image(qb_id)
    download_player_image(qb_id)
    time.sleep(5)
