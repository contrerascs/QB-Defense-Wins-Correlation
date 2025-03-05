import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def render_pass_performance_plot(qb_data, league_avg_data, selected_qb, selected_season):
    # Filtrar los datos del QB
    qb_stats = qb_data[(qb_data["Player"] == selected_qb) & (qb_data["Season"] == selected_season)]
    if qb_stats.empty:
        st.warning("No hay datos disponibles para este QB en la temporada seleccionada.")
        return

    qb_stats = qb_stats.iloc[0]

    # Definir las métricas a comparar
    metrics = ["Y/A", "AY/A", "Y/C"]
    metric_labels = ["Yardas por Intento", "Yardas Ajustadas por Intento", "Yardas por Recepción"]

    # Obtener el promedio de la liga
    league_avg = league_avg_data[league_avg_data["Y/A", "AY/A", "Y/C"] == selected_season].mean()

    # Datos del gráfico
    player_values = [qb_stats[m] for m in metrics]
    league_values = [league_avg[m] for m in metrics]

    # Crear el gráfico de barras con sombras
    fig = go.Figure()

    # Barras de fondo (promedio de la liga)
    fig.add_trace(go.Bar(
        x=metric_labels,
        y=league_values,
        name="Promedio de la Liga",
        marker_color="gray",
        opacity=0.5  # Se usa opacidad para dar efecto de sombra
    ))

    # Barras del jugador
    fig.add_trace(go.Bar(
        x=metric_labels,
        y=player_values,
        name=f"{selected_qb}",
        marker_color="blue"
    ))

    fig.update_layout(
        title=f"Desempeño en el Pase de {selected_qb} vs Promedio de la Liga ({selected_season})",
        xaxis_title="Métrica",
        yaxis_title="Valor",
        template="plotly_dark",
        barmode="overlay"  # Se superponen las barras
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
