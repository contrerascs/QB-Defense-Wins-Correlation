import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Cargar los datasets
qb_df = pd.read_csv("data/processed/qb_stats.csv")
defense_df = pd.read_csv("data/processed/defense_stats.csv")
kickers_df = pd.read_csv("data/processed/kickers_stats.csv")

# Título del proyecto
st.title("📊 NFL QB Performance Dashboard")
st.write("Este dashboard muestra cómo las victorias no son una estadística exclusiva del QB.")

# Barra de búsqueda de QBs
qb_list = qb_df["Player"].unique()
selected_qb = st.selectbox("Selecciona un QB", qb_list)

# Filtrar datos del QB seleccionado
qb_data = qb_df[qb_df["Player"] == selected_qb]
qb_id = qb_data["Player-additional"].iloc[0]

# Verificar si la imagen ya existe
if os.path.exists(f"data/images/{qb_id}.jpg"):
    # Mostrar imagen del QB
    image_path = f"data/images/{qb_id}.jpg"
else:
    image_path = "data/images/Not_found_image.jpg"

st.image(image_path, width=150, caption=selected_qb)

# Seleccionar temporada específica o ver toda la carrera
season_options = ["Toda la carrera"] + sorted(qb_data["Season"].unique().tolist(), reverse=True)
selected_season = st.selectbox("Selecciona una temporada", season_options)

if selected_season == "Toda la carrera":
    qb_data = qb_data.groupby("Player").sum(numeric_only=True).reset_index()
else:
    qb_data = qb_data[qb_data["Season"] == selected_season]

# Mostrar estadísticas básicas
yards = qb_data["Yds"].sum()
tds = qb_data["TD"].sum()
ints = qb_data["Int"].sum()
st.metric(label="Yardas Totales", value=f"{yards:,}")
st.metric(label="Touchdowns", value=tds)
st.metric(label="Intercepciones", value=ints)

# Mostrar estadísticas detalladas en una tabla
st.write("### Estadísticas detalladas")
st.dataframe(qb_data)

# TODO: Agregar visualizaciones y correlaciones con defensa y kickers
