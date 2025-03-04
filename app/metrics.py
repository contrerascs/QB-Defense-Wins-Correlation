# app/metrics.py
import streamlit as st

def render_metrics(qb_data):
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    
    with c1:
        games = int(qb_data["GS"].sum())
        st.metric(label="Partidos Jugados", value=f"{games:,}")
    
    with c2:
        atts = int(qb_data["Att"].sum())
        st.metric(label="Intentos de Pase", value=f"{atts:,}")
    
    with c3:
        cmp_value = float(qb_data['Cmp%'].iloc[0])
        st.metric(label='Cmp%', value=f"{round(cmp_value, 2)}%")
    
    with c4:
        yards = int(qb_data["Yds"].sum())
        st.metric(label="Yardas Totales", value=f"{yards:,}")
    
    with c5:
        tds = int(qb_data["TD"].sum())
        st.metric(label="Touchdowns", value=tds)
    
    with c6:
        ints = int(qb_data["Int"].sum())
        st.metric(label="Intercepciones", value=ints)
    
    with c7:
        rating = float(qb_data['Rate'].iloc[0])
        st.metric(label='Rating', value=round(rating, 2))