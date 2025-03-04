# app/main.py
import streamlit as st
import pandas as pd
import os
from app.plots import calculate_custom_epa
from app.sidebar import render_sidebar
from app.metrics import render_metrics
from app.plots import render_plots

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
selected_season, qb_data = render_sidebar(qb_data, selected_qb, qb_id, image_path)

# Mostrar métricas básicas en la parte principal
render_metrics(qb_data)

# Si se seleccionó una temporada específica, renderizamos las gráficas
if selected_season != "Toda la carrera":
    render_plots(qb_data, selected_qb, selected_season)
    st.text(calculate_custom_epa(qb_data, selected_qb, selected_season))
else:
    pass
