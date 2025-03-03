# app/sidebar.py
import streamlit as st
from scripts.Filters import extract_awards, teams

def render_sidebar(qb_data, selected_qb, qb_id, image_path):
    with st.sidebar:
        col1, col2 = st.columns(2)
        with col1:
            st.header('Quarterback')
            st.image(image_path, width=150)
            st.subheader(selected_qb)
        with col2:
            st.header(":green[Equipos]", divider="gray")
            for team in teams(qb_id, qb_data):
                st.text(team)
            
            st.subheader(':green[Temporadas]', divider="gray")
            start_qb = qb_data['Season'].min()
            end_qb = qb_data['Season'].max()
            st.text(f'{start_qb} - {end_qb}')
            
            # Mostrar premios individuales
            premios = extract_awards(selected_qb)
            st.subheader(":green[Premios]", divider="gray")
            for premio, cantidad in premios.items():
                if cantidad > 0:
                    st.text(f"{premio}: {cantidad}")
        
        # Selección de temporada
        season_options = ["Toda la carrera"] + sorted(qb_data["Season"].unique().tolist(), reverse=True)
        selected_season = st.selectbox("Selecciona una temporada", season_options)
        
        # Filtrado según la temporada seleccionada
        if selected_season == "Toda la carrera":
            # Agrupar datos y calcular promedios reales para algunas columnas
            qb_data = qb_data.groupby("Player").sum(numeric_only=True).reset_index()
            qb_data["Rate"] = qb_data["Rate"].mean()
            qb_data["Cmp%"] = qb_data["Cmp%"].mean()
        else:
            qb_data = qb_data[qb_data["Season"] == selected_season]
            
    return selected_season, qb_data