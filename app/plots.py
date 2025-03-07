# app/plots.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

def render_plots(qb_data, selected_qb, selected_season,season_df):
    # Asegurar que la columna Season es string y ordenar
    if "Season" in qb_data.columns:
        qb_data["Season"] = qb_data["Season"].astype(str)
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

    # Estadísticas clave a normalizar
    pass_stats_to_normalize = ["AY/A","Y/A", "Cmp%", "Y/G","Att"]
    
    metric_names = {
        "AY/A": "Adj-Yds/att",
        "Y/A": "Yds/att",
        "Y/G": "Yds/Game",
        "Att": "Atts"
    }

    # Diccionario para almacenar valores normalizados con nombres descriptivos
    normalized_stats = {}

    for stat in pass_stats_to_normalize:
        if stat in season_df.columns:
            min_val = season_df[stat].min()
            max_val = season_df[stat].max()
            
            if max_val - min_val != 0:  # Evitar divisiones por cero
                normalized_stats[metric_names.get(stat, stat)] = (qb_data[stat].values[0] - min_val) / (max_val - min_val) * 100
            else:
                normalized_stats[metric_names.get(stat, stat)] = 50  # Valor neutral si no hay variación

    # Convertir a listas para la gráfica
    categories = list(normalized_stats.keys())
    values = list(normalized_stats.values())

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

    # Estilizar el gráfico
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],  # Normalizado de 0 a 100
                tickmode='array',
                tickvals=[0, 25, 50, 75, 100]
            )
        ),
        showlegend=True,
        title=f'Puntuación en Precisión y Volumen de pase - {selected_qb} ({selected_season})',
        template='plotly_dark',
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
    stats_to_normalize = ['Cmp%', 'TD%', 'Int%', 'Rate', 'Yds']
    
    # Diccionario para almacenar valores normalizados
    normalized_stats = {}
    
    for stat in stats_to_normalize:
        if stat in season_df.columns:
            min_val = season_df[stat].min()
            max_val = season_df[stat].max()
            
            if max_val - min_val != 0:  # Evitar divisiones por cero
                normalized_stats[stat] = (qb_data[stat].values[0] - min_val) / (max_val - min_val) * 100
            else:
                normalized_stats[stat] = 50  # Valor neutral si no hay variación
    
    # Crear el gráfico de barras con Plotly
    fig = go.Figure(data=[go.Bar(
        x=list(normalized_stats.keys()),
        y=list(normalized_stats.values()),
        marker=dict(color='#1CB698', opacity=0.9)
    )])
    
    # Estilizar el gráfico
    fig.update_layout(
        title=f'Comparación Normalizada - {selected_qb} ({selected_season})',
        xaxis_title='Estadísticas',
        yaxis_title='Valor Normalizado (0-100)',
        yaxis=dict(range=[0, 100]),
        #plot_bgcolor='white',
        xaxis=dict(tickangle=45),
        template='plotly_white',
        width=400,  # Ajusta el ancho en píxeles
        height=450
    )

    # Mostrar las gráficas en Streamlit
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie, use_container_width=True)
        st.plotly_chart(fig_sk_rate, use_container_width=False)

    with c2:
        st.plotly_chart(fig_radar, use_container_width=True)
        st.plotly_chart(fig, use_container_width=False)
    