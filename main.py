# app/main.py
import streamlit as st
from app.sidebar import render_sidebar
from app.season_metrics import render_season_metrics
from app.season_plots import render_plots
from app.carrer_metrics import render_carrer_metrics
from helpers.data_loader import load_datasets
from app.carrer_plots import render_carrer_plots

# Cargar los datasets
qb_df,defense_df,kickers_df = load_datasets()

# Configuración inicial de Streamlit
st.set_page_config(
    page_title='QB vs DEFENSE - STATS',
    page_icon=':football:',
    layout='wide',
    initial_sidebar_state='expanded',
    
)

st.title('Analiza las estadísticas de tu QB favorito')

# Seleccionar QB
qb_list = qb_df["Player"].unique()
selected_qb = st.selectbox("Selecciona un QB", qb_list)

# Filtrar datos del QB seleccionado y obtener el ID
qb_data = qb_df[qb_df["Player"] == selected_qb]
qb_id = qb_data["Player-additional"].iloc[0]

# Renderizar la barra lateral y filtrar por temporada
selected_season, qb_data_in_season = render_sidebar(qb_df, qb_data, selected_qb, qb_id)

# Si se seleccionó una temporada específica, renderizamos las gráficas
if selected_season != "Toda la carrera":
    # Mostrar métricas básicas en la parte principal
    season_defense = defense_df[defense_df["Season"] == selected_season]
    render_season_metrics(qb_data_in_season, qb_df, selected_season, selected_qb, season_defense)
    # Mostrar gráficos del QB
    season_df = qb_df[qb_df["Season"] == selected_season]
    render_plots(qb_data_in_season, selected_qb, selected_season,season_df,season_defense)
else:
    render_carrer_metrics(qb_data,selected_qb)
    render_carrer_plots(qb_data,selected_qb,defense_df,qb_df)
