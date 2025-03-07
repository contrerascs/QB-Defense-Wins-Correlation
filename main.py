# app/main.py
import streamlit as st
import pandas as pd
import os
from app.sidebar import render_sidebar
from app.season_metrics import render_season_metrics
from app.plots import render_plots
from app.carrer_metrics import render_carrer_metrics

# Cargar los datasets
qb_df = pd.read_csv(os.path.join("data", "processed", "qb_stats.csv"))
defense_df = pd.read_csv(os.path.join("data", "processed", "defense_stats.csv"))
kickers_df = pd.read_csv(os.path.join("data", "processed", "kickers_stats.csv"))

# Configuración inicial de Streamlit
st.set_page_config(
    page_title='QB STATS',
    page_icon=':football:',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.title('Analiza las estadísticas de tu QB favorito')

# Seleccionar QB
qb_list = qb_df["Player"].unique()
selected_qb = st.selectbox("Selecciona un QB", qb_list)

# Filtrar datos del QB seleccionado y obtener el ID
qb_data = qb_df[qb_df["Player"] == selected_qb]
qb_id = qb_data["Player-additional"].iloc[0]

# Verificar existencia de la imagen
image_path = os.path.join("data", "images", f"{qb_id}.jpg")
if not os.path.exists(image_path):
    image_path = os.path.join("data", "images", "Not_found_image.jpg")

# Renderizar la barra lateral y filtrar por temporada
selected_season, qb_data = render_sidebar(qb_df, qb_data, selected_qb, qb_id, image_path)

# Si se seleccionó una temporada específica, renderizamos las gráficas
if selected_season != "Toda la carrera":
    # Mostrar métricas básicas en la parte principal
    season_defense = defense_df[defense_df["Season"] == selected_season]
    render_season_metrics(qb_data, qb_df, selected_season, selected_qb, season_defense)
    # Mostrar gráficos del QB
    season_df = qb_df[qb_df["Season"] == selected_season]
    render_plots(qb_data, selected_qb, selected_season,season_df)
else:
    render_carrer_metrics(qb_data)
