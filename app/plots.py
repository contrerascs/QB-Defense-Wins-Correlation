# app/plots.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from helpers.data_utils import normalize_stats_plots,calculate_qb_metrics,normalize_stats_defense_plots
from helpers.data_filter import team_for_season

def render_plots(qb_data, selected_qb, selected_season,season_df,season_defense):
    # Asegurar que la columna Season es string y ordenar
    if "Season" in qb_data.columns:
        qb_data["Season_str"] = qb_data["Season"].astype(str)  # Nueva columna
        qb_data = qb_data.sort_values("Season")
    
    # Rellenar NaN para evitar errores en la gráfica
    qb_data["Yds"] = qb_data["Yds"].fillna(0)
    qb_data["TD"] = qb_data["TD"].fillna(0)
    qb_data["Int"] = qb_data["Int"].fillna(0)
    
    qb_stats = qb_data.iloc[0]  # Como es una temporada específica, se espera un solo registro
    
    # Gráfica de pastel: Pases Completos vs Incompletos
    completos = qb_stats["Cmp%"]
    incompletos = 100 - completos
    labels = ["Pases Completos", "Pases Incompletos"]
    values = [completos, incompletos]
    colors = ["#1CB698", "#0a4237"]
    
    fig_pie = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors),
        textinfo="percent"
    ))
    fig_pie.update_layout(
        title=f"Porcentaje de Pases Completos de {selected_qb} en {selected_season}",
        template="plotly_dark"
    )

    # Obtener métricas normalizadas del QB seleccionado
    qb_metrics = calculate_qb_metrics(season_df, selected_qb)

    # Convertir a listas para la gráfica
    categories = list(qb_metrics.keys())
    values = list(qb_metrics.values())

    # Cerrar el gráfico conectando el último punto con el primero
    values.append(values[0])
    categories.append(categories[0])

    # Crear el gráfico de radar con Plotly
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=f'{selected_qb} ({selected_season})',
        line=dict(color='#1CB698'),
        fillcolor='rgba(28, 182, 152, 0.3)'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"Fortalezas de {selected_qb} en {selected_season}",
        template='plotly_dark'
    )

    ## 🔹 Gauge Chart: Porcentaje de Capturas (Sk%)
    fig_sk_rate = go.Figure(go.Indicator(  
    mode="gauge+number",  
    value=qb_stats["Sk%"],  
    number={"suffix": "%"},  
    gauge={  
        "axis": {"range": [0, 15],
                 "tickvals": [0, 3, 6, 9, 12, 15],
                 },  # Rango de referencia para Sk%  
        "bar": {"color": "white"},  # Color de la barra que representa el valor  
        "steps": [  
            {"range": [0, 3], "color": "#1CB698"},  # Rango de 0 a 5
            {"range": [3, 6], "color": "#189a80"},  
            {"range": [6, 9], "color": "#15846e"}, # Rango de 5 a 10
            {"range": [9, 12], "color": "#116e5c"},  
            {"range": [12, 15], "color": '#0a4237'}    # Rango de 10 a 15  
        ],  
        "threshold": {  
            "line": {"color": "white", "width": 4},  # Línea de umbral  
            "thickness": 1,  
            "value": qb_stats["Sk%"]  
            }  
        }  
    ))
    fig_sk_rate.update_layout(
        title=f"Porcentaje de Capturas de {selected_qb} en {selected_season}",
        template="plotly_dark",
        width=400,  # Ajusta el ancho en píxeles
        height=450
        )
    
    # Estadísticas clave a normalizar 
    pass_stats_to_normalize = ["Yds","TD", "Int","Att","1D"]
    defense_stats_to_normalize = ['Passing Yds','Passing TD','Int','Passing Att','Passing 1stD']

    metric_names = {
        "Yds": "Air Yds",
        "TD": "TDs",
        "Int": "Entregas",
        "Att": "Atts",
        "1D": "Passing 1stD"
    }
    metric_names_defense = {
        "Passing Yds": "Air Yds",
        "Passing TD": "TDs",
        "Int": "Entregas",
        "Passing Att": "Atts",
        "Passing 1stD": "Passing 1stD"
    }

    team = team_for_season(selected_qb, qb_data, selected_season)
    # Filtrar las estadísticas de la defensa del equipo
    defense_stats = season_defense[season_defense["Team"] == team]
    # Diccionario para almacenar valores normalizados de la defensa
    normalized_defense_stats = {}

    # Normalizar las estadísticas de la defensa (invertir=True)
    for stat in defense_stats_to_normalize:
        if stat in season_defense.columns:
            normalized_value = normalize_stats_defense_plots(season_defense, stat, team, invert=True)  # Invertir la normalización
            if normalized_value is not None:
                normalized_defense_stats[metric_names_defense.get(stat, stat)] = normalized_value

    # Diccionario para almacenar valores normalizados con nombres descriptivos
    normalized_stats = {}

    # Normalizar las estadísticas usando la función
    for stat in pass_stats_to_normalize:
        if stat in season_df.columns:
            # Normalizar el valor del jugador
            normalized_value = normalize_stats_plots(season_df, stat, selected_qb)
            if normalized_value is not None:
                normalized_stats[metric_names.get(stat, stat)] = normalized_value

    # Convertir a listas para la gráfica
    categories = list(normalized_stats.keys())
    values = list(normalized_stats.values())

    # Convertir a listas para la gráfica
    defense_categories = list(normalized_defense_stats.keys())
    defense_values = list(normalized_defense_stats.values())

    # Cerrar el gráfico conectando el último punto con el primero
    defense_values.append(defense_values[0])
    defense_categories.append(defense_categories[0])

    # Cerrar el gráfico conectando el último punto con el primero
    values.append(values[0])
    categories.append(categories[0])

    # Crear el gráfico de radar con Plotly
    fig_vs = go.Figure()

    fig_vs.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=f'{selected_qb} ({selected_season})',
        line=dict(color='#1CB698'),
        fillcolor='rgba(28, 182, 152, 0.3)'
    ))

    # Gráfica de la defensa
    fig_vs.add_trace(go.Scatterpolar(
        r=defense_values,
        theta=defense_categories,
        fill='toself',
        name=f'Defensa',
        line=dict(color='#FF6B6B'),
        fillcolor='rgba(255, 107, 107, 0.3)'
    ))

    # Estilizar el gráfico
    fig_vs.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],  # Normalizado de 0 a 100
                tickmode='array',
                tickvals=[0, 25, 50, 75, 100]
            )
        ),
        showlegend=True,
        title=f'Puntuación de {selected_qb} y {team} en ({selected_season})',
        template='plotly_dark',
    )

    # Mostrar las gráficas en Streamlit
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie, use_container_width=True)
        st.plotly_chart(fig_sk_rate, use_container_width=False)

    with c2:
        st.plotly_chart(fig_radar, use_container_width=True)
        st.plotly_chart(fig_vs, use_container_width=True)
    