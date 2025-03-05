# app/plots.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def render_plots(qb_data, selected_qb, selected_season):
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
    colors = ["blue", "red"]
    
    fig_pie = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors),
        textinfo="percent"
    ))
    fig_pie.update_layout(
        title=f"Porcentaje de Pases Completos de {selected_qb} en {selected_season}",
        template="plotly_dark"
    )
    
    # Gráfica de barras: Clutch Performance (4QC y GWD)
    clutch_data = pd.DataFrame({
        "Métrica": ["4QC", "GWD"],
        "Valor": [qb_stats["4QC"], qb_stats["GWD"]]
    })
    
    fig_clutch = px.bar(
        clutch_data,
        x="Valor",
        y="Métrica",
        text="Valor",
        title=f"Clutch Performance de {selected_qb} en {selected_season}",
        color="Métrica",
        color_discrete_map={"4QC": "blue", "GWD": "green"}
    )
    fig_clutch.update_layout(
        xaxis_title="Cantidad",
        yaxis_title="Métrica",
        template="plotly_dark"
    )

    # Gráfica de comparación: TD%, Int%, NY/A, ANY/A
    comparison_data = pd.DataFrame({
        "Estadística": [
            "TD%", 
            "Int%", 
            "NY/A", 
            "ANY/A"
        ],
        "Valor": [
            qb_stats["TD%"], 
            qb_stats["Int%"], 
            qb_stats["NY/A"], 
            qb_stats["ANY/A"]
        ]
    })

    fig_comparison = px.bar(
        comparison_data,
        x="Estadística",
        y="Valor",
        text="Valor",
        title=f"Comparación de Estadísticas de {selected_qb} en {selected_season}",
        color="Estadística",
        color_discrete_map={
            "TD%": "green", 
            "Int%": "red",
            "NY/A": "blue",
            "ANY/A": "purple"
        }
    )
    fig_comparison.update_layout(
        xaxis_title="Métrica",
        yaxis_title="Valor",
        template="plotly_dark"
    )

    #Gráfica: Desempeño en el pase
    pass_performance_data = pd.DataFrame({
        "Métrica": [ "Y/A", "AY/A", "Y/C"],
        "Valor": [qb_stats["Y/A"], qb_stats["AY/A"], qb_stats["Y/C"]]
    })

    fig_pass_performance = px.bar(
        pass_performance_data,
        x="Métrica",
        y="Valor",
        text="Valor",
        title=f"Desempeño en el Pase de {selected_qb} en {selected_season}",
        color="Métrica",
        color_discrete_map={ 
            "Y/A": "green", 
            "AY/A": "purple", 
            "Y/C": "orange"
        }
    )
    fig_pass_performance.update_layout(
        xaxis_title="Métrica",
        yaxis_title="Valor",
        template="plotly_dark"
    )

    ## 🔹 Gráfica de barras: Capturas y Yardas Perdidas
    pressure_data = pd.DataFrame({
        "Métrica": ["Capturas", "Yardas Perdidas"],
        "Valor": [qb_stats["Sk"], qb_stats["Yds.1"]]
    })

    fig_pressure = px.bar(
        pressure_data,
        x="Métrica",
        y="Valor",
        text="Valor",
        title=f"Presión sobre {selected_qb} en {selected_season}",
        color="Métrica",
        color_discrete_map={"Capturas": "red", "Yardas Perdidas": "orange"}
    )
    fig_pressure.update_layout(
        xaxis_title="Métrica",
        yaxis_title="Cantidad",
        template="plotly_dark"
    )

    ## 🔹 Gauge Chart: Porcentaje de Capturas (Sk%)
    fig_sk_rate = go.Figure(go.Indicator(  
    mode="gauge+number",  
    value=qb_stats["Sk%"],  
    number={"suffix": "%"},  
    gauge={  
        "axis": {"range": [0, 15]},  # Rango de referencia para Sk%  
        "bar": {"color": "white"},  # Color de la barra que representa el valor  
        "steps": [  
            {"range": [0, 5], "color": "green"},  # Rango de 0 a 5  
            {"range": [5, 10], "color": "yellow"}, # Rango de 5 a 10  
            {"range": [10, 15], "color": "red"}    # Rango de 10 a 15  
        ],  
        "threshold": {  
            "line": {"color": "red", "width": 4},  # Línea de umbral  
            "thickness": 1,  
            "value": qb_stats["Sk%"]  
            }  
        }  
    ))
    fig_sk_rate.update_layout(
        title=f"Porcentaje de Capturas de {selected_qb} en {selected_season}",
        template="plotly_dark")

    # Mostrar las gráficas en Streamlit
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie, use_container_width=True)
        st.plotly_chart(fig_sk_rate, use_container_width=True)
        st.plotly_chart(fig_pressure, use_container_width=True)

    with c2:
        st.plotly_chart(fig_pass_performance, use_container_width=True)
        st.plotly_chart(fig_comparison, use_container_width=True)
    
def calculate_custom_epa(qb_data, selected_qb, selected_season):
    # Asegurar que la columna Season es string y ordenar
    if "Season" in qb_data.columns:
        qb_data["Season"] = qb_data["Season"].astype(str)
        qb_data = qb_data.sort_values("Season")
    
    # Rellenar NaN para evitar errores en la gráfica
    qb_data["Yds"] = qb_data["Yds"].fillna(0)
    qb_data["TD"] = qb_data["TD"].fillna(0)
    qb_data["Int"] = qb_data["Int"].fillna(0)
    
    qb_stats = qb_data.iloc[0]  # Como es una temporada específica, se espera un solo registro
    
    # Factores ponderados para calcular EPA/play personalizado
    epa = (
        (qb_stats["ANY/A"] * 0.4) +  # Yardas netas ajustadas por intento
        (qb_stats["NY/A"] * 0.3) -   # Yardas netas por intento
        ((100 - qb_stats['Cmp%']) * 0.2) +
        (qb_stats["TD%"] * 0.2) -    # Porcentaje de touchdowns
        (qb_stats["Int%"] * 0.4) +   # Penalización por intercepciones
        (qb_stats["Succ%"] * 0.2) +  # Porcentaje de jugadas exitosas
        (qb_stats["Rate"] * 0.1) +   # Rating del QB
        (qb_stats["4QC"] * 0.15) +   # Drives de remontada en el 4° cuarto
        (qb_stats["GWD"] * 0.15)     # Drives ganadores
    )

    return round((epa/100), 2)  # Redondear a dos decimales
