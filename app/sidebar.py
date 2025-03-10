# app/sidebar.py
import streamlit as st
from helpers.data_utils import get_image_path
from helpers.data_filter import teams,extract_awards

def render_player_info(col, selected_qb, qb_id):
    """Renderiza la información del jugador en la barra lateral."""
    with col:
        st.header('Quarterback')
        image_path = get_image_path(qb_id)
        st.image(image_path, width=150)
        st.subheader(selected_qb)

def render_teams_info(col, qb_id, qb_data):
    """Renderiza la información de los equipos en la barra lateral."""
    with col:
        st.header(":gray[Equipos]", divider="gray")
        for team in teams(qb_id, qb_data):
            st.text(team)

def render_seasons_info(col, qb_data):
    """Renderiza la información de las temporadas en la barra lateral."""
    with col:
        st.subheader(':gray[Temporadas]', divider="gray")
        start_qb = qb_data['Season'].min()
        end_qb = qb_data['Season'].max()
        st.text(f'{start_qb} - {end_qb}')

def render_awards_info(col, selected_qb):
    """Renderiza la información de los premios en la barra lateral."""
    with col:
        premios = extract_awards(selected_qb)
        st.subheader(":gray[Premios]", divider="gray")
        for premio, cantidad in premios.items():
            if cantidad > 0:
                st.text(f"{premio}: {cantidad}")

def filter_qb_data(qb_data, selected_season, qb_df, selected_qb):
    """Filtra los datos del QB según la temporada seleccionada."""
    if selected_season == "Toda la carrera":
        qb_data = qb_data.groupby("Player").sum(numeric_only=True).reset_index()
        qb_data["Rate"] = qb_df[qb_df["Player"] == selected_qb]["Rate"].mean()
        qb_data["Cmp%"] = qb_df[qb_df["Player"] == selected_qb]["Cmp%"].mean()
    else:
        qb_data = qb_data[qb_data["Season"] == selected_season]
    return qb_data

def render_sidebar(qb_df, qb_data, selected_qb, qb_id):
    """Renderiza la barra lateral completa."""
    with st.sidebar:
        st.image('assets/logo.png',use_container_width=True)
        col1, col2 = st.columns(2)

        # Información del jugador
        render_player_info(col1, selected_qb, qb_id)

        # Información de equipos, temporadas y premios
        render_teams_info(col2, qb_id, qb_data)
        render_seasons_info(col2, qb_data)
        render_awards_info(col2, selected_qb)

        # Selección de temporada
        season_options = ["Toda la carrera"] + sorted(qb_data["Season"].unique().tolist(), reverse=True)
        selected_season = st.selectbox("Selecciona una temporada", season_options)

        # Filtrar datos según la temporada seleccionada
        qb_data = filter_qb_data(qb_data, selected_season, qb_df, selected_qb)
        
    return selected_season, qb_data