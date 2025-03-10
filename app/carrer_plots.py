# app/season_plots.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from app.season_metrics import calculate_defense_rank,calculate_qb_rank

def render_carrer_plots(qb_data,selected_qb,df_def_stats,df_qb_stats):
    # Agrupar por temporada y sumar yardas
    qb_season_stats = qb_data.groupby("Season")["Yds"].sum().reset_index()

    # Ordenar por temporada
    qb_season_stats = qb_season_stats.sort_values(by="Season")

    # Crear la gráfica interactiva con Plotly
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=qb_season_stats["Season"],
        y=qb_season_stats["Yds"],
        mode="lines+markers",
        line=dict(color="#1CB698", width=3),
        marker=dict(size=8, color="#7bead4"),
        name=selected_qb
    ))

    fig.update_layout(
    title=f"Evolución de Yardas Lanzadas de {selected_qb} por Temporada",
    xaxis_title="Temporada",
    yaxis_title="Yardas Lanzadas",
    xaxis=dict(
        showgrid=False,
        linecolor='rgba(0,0,0,0)',  # Color de la línea del eje X con transparencia
        linewidth=2  # Grosor de la línea del eje X
    ),
    yaxis=dict(
        showgrid=True,
        #gridcolor="lightgray",
        linecolor='rgba(0,0,0,0)',  # Color de la línea del eje Y con transparencia
        linewidth=2  # Grosor de la línea del eje Y
        ),
    template="plotly_dark"
    )

    # Agrupar por temporada y calcular estadísticas
    qb_season_stats = qb_data.groupby("Season").agg({
        "TD%": "mean",  # Tomamos el promedio del porcentaje de TDs
        "Int%": "mean",  # Promedio de porcentaje de intercepciones
        "Att": "sum"  # Sumar los intentos de pase para el tamaño de la burbuja
    }).reset_index()

    # Definir una lista de colores personalizados (HEX o RGB)
    custom_colors = [
        "#d3f8f1", "#bdf5ea", "#a7f1e2", "#91eedb", "#7bead4", 
        "#65e7cd", "#4fe3c6", "#38e0bf", "#22ddb7", "#1fc7a5", 
        "#1cb698", "#1cb093", "#189a80", "#15846e", "#116e5c"
    ]

    # Crear la gráfica de burbujas
    fig_buble = px.scatter(
        qb_season_stats,
        x="Int%",
        y="TD%",
        size="Att",  # Tamaño de la burbuja basado en intentos de pase
        color="Season",  # Diferenciar temporadas por color
        hover_name="Season",  # Mostrar la temporada en el hover
        title=f"TD% vs INT% de {selected_qb} por Temporada",
        labels={"TD%": "Porcentaje de TDs", "Int%": "Porcentaje de Intercepciones"},
        template="plotly_dark",
        color_continuous_scale=custom_colors  # Aplicar colores personalizados
    )

    # Ajustar diseño
    fig_buble.update_layout(
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True),
        showlegend=True
    )

    #QB VS DEFENSE
    # Obtener el ranking del QB y el ranking de su defensa por temporada
    seasons = sorted(df_qb_stats["Season"].unique())  # Lista de temporadas ordenadas
    qb_ranks = [calculate_qb_rank(df_qb_stats[df_qb_stats["Season"] == season], selected_qb) for season in seasons]
    defense_ranks = [calculate_defense_rank(df_def_stats[df_def_stats["Season"] == season], season, selected_qb, df_qb_stats) for season in seasons]

    # Crear DataFrame con los rankings
    ranking_data = pd.DataFrame({"Season": seasons, "QB_Rank": qb_ranks, "Defense_Rank": defense_ranks})

    # Filtrar solo las temporadas en las que el QB jugó (donde no hay valores None)
    ranking_data = ranking_data.dropna()

    # Crear la figura con Plotly
    fig_qb_vs_df = go.Figure()

    # Línea del QB
    fig_qb_vs_df.add_trace(go.Scatter(
        x=ranking_data["Season"],
        y=ranking_data["QB_Rank"],
        mode="lines+markers",
        name="QB Ranking",
        line=dict(color="#1CB698", width=3),
        marker=dict(size=8, symbol="circle", color="#7bead4"),
    ))

    # Línea de la Defensa
    fig_qb_vs_df.add_trace(go.Scatter(
        x=ranking_data["Season"],
        y=ranking_data["Defense_Rank"],
        mode="lines+markers",
        name="Defense Ranking",
        line=dict(color="#bdf5ea", width=3, dash="dash"),
        marker=dict(size=8, symbol="square", color="#189a80")
    ))

    # Configuración de la gráfica
    fig_qb_vs_df.update_layout(
        title=f"Comparación del Ranking de {selected_qb} y sus Defensivas durante su carrera",
        xaxis=dict(title="Temporada", tickmode="linear"),
        yaxis=dict(
            title="Ranking",
            autorange="reversed",  # Invertir el eje Y
            tickvals=list(range(1, 33, 3)),  # Mostrar un valor cada 3 rankings
            range=[32, 0.5]  # Establecer el rango manualmente (de 32 a 0.5)
        ),
        legend=dict(title="Categoría"),
        template="plotly_dark"
    )

    # Crear la gráfica de barras
    fig_TD = px.bar(
        qb_data,
        x="Season",
        y="TD",
        text="TD",
        title=f"Touchdowns por Temporada - {selected_qb}",
        labels={"Season": "Temporada", "TD": "Touchdowns"},
        color="TD",
        color_continuous_scale=custom_colors,  # Escala de colores (se puede cambiar a 'reds', 'viridis', etc.)
    )

    # Mejorar el diseño
    fig_TD.update_traces(texttemplate="%{text}", textposition="outside", marker=dict(line=dict(color="black", width=1)))
    fig_TD.update_layout(xaxis=dict(type="category"), template="plotly_dark")

    # Crear la gráfica de dispersión
    fig_sacks = px.scatter(
        qb_data,
        x="Sk",  # Número de sacks recibidos
        y="Y/A",  # Yardas por intento
        size="TD",  # Tamaño de burbuja según touchdowns lanzados
        color="Season",  # Diferenciar por temporada
        title=f"Relación entre Sacks Recibidos y Yardas por Intento - {selected_qb}",
        labels={"Sk": "Sacks Recibidos", "Y/A": "Yardas por Intento"},
        hover_name="Season",
        color_continuous_scale=custom_colors
    )

    # Mejorar diseño
    fig_sacks.update_layout(template="plotly_dark")

    # Cada tupla contiene (posición, color), donde la posición va de 0 a 1
    custom_scale = [(i / (len(custom_colors) - 1), color) for i, color in enumerate(custom_colors)]

    # Seleccionar las columnas relevantes
    heatmap_data = qb_data[['Season', 'Att', 'Cmp', 'Y/G']]

    # Crear la matriz de valores para el heatmap
    values = heatmap_data.set_index('Season').values

    # Crear el heatmap
    fig_map = go.Figure(data=go.Heatmap(
        z=values,  # Valores de la matriz
        x=['Intentos', 'Completos', 'Yds Juego'],  # Métricas
        y=heatmap_data['Season'],  # Temporadas
        colorscale=custom_scale,  # Usar la escala personalizada (correcta propiedad)
        text=values,  # Mostrar los valores en las celdas
        texttemplate="%{text:.2f}",  # Formato de los valores
        colorbar=dict(title="Valor")
    ))

    # Personalizar el diseño
    fig_map.update_layout(
        title=f"Evaluación de Temporadas de {selected_qb}",
        xaxis_title="Métrica",
        yaxis_title="Temporada",
        template="plotly_dark"
    )

    # Mostrar las gráficas en Streamlit
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.plotly_chart(fig_buble, use_container_width=True)

    st.plotly_chart(fig_qb_vs_df, use_container_width=True)

    # Mostrar las gráficas en Streamlit
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_TD, use_container_width=True)

    with c2:
        st.plotly_chart(fig_map, use_container_width=True)