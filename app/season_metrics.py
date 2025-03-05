# app/metrics.py
import streamlit as st
import pandas as pd
from scripts.Filters import teams

def calculate_position(df, player, metric):
    df = df[df["Att"] > 110]
    df = df.sort_values(by=metric, ascending=False).reset_index(drop=True)
    df[metric + "_rank"] = df[metric].rank(method="min", ascending=False)
    return df.loc[df["Player"] == player, metric + "_rank"].values[0]

def calculate_qb_rank(df, player):
    df = df.sort_values(by=['Att','Cmp%','Yds','TD','TD%'], ascending=[False, False, False,False, False]).reset_index(drop=True)
    df["QB_Rank"] = df.index + 1
    return df.loc[df["Player"] == player, "QB_Rank"].values[0]

def calculate_defense_rank(df, team):
    df = df.sort_values(by=["Points Allowed", "Yards Allowed"], ascending=[True, True]).reset_index(drop=True)
    df["Defense_Rank"] = df.index + 1
    return df.loc[df["Team"] == team, "Defense_Rank"].values[0]

def render_season_metrics(qb_data, qb_df, selected_season, selected_qb):
    if selected_season == "Toda la carrera":
        season_df = qb_df.groupby("Player").sum(numeric_only=True).reset_index()
    else:
        season_df = qb_df[qb_df["Season"] == selected_season]

    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)

    with c1:
        games = int(qb_data["GS"].sum())
        st.metric("Partidos Jugados", f"{games:,}")

    with c2:
        atts = int(qb_data["Att"].sum())
        rank = calculate_position(season_df, selected_qb, "Att")
        if rank >= 16:
            st.metric("Intentos de Pase", f"{atts:,}", f"{(-int(rank))}º")
        else:
            st.metric("Intentos de Pase", f"{atts:,}", f"{int(rank)}º")

    with c3:
        cmp_value = float(qb_data['Cmp%'].iloc[0])
        rank = calculate_position(season_df, selected_qb, "Cmp%")
        if rank >= 16:
            st.metric('Cmp%', f"{round(cmp_value, 2)}%", f"{(-int(rank))}º")
        else:
            st.metric('Cmp%', f"{round(cmp_value, 2)}%", f"{int(rank)}º")

    with c4:
        yards = int(qb_data["Yds"].sum())
        rank = calculate_position(season_df, selected_qb, "Yds")
        if rank >= 16:
            st.metric("Yardas Totales", f"{yards:,}", f"{(-int(rank))}º")
        else:
            st.metric("Yardas Totales", f"{yards:,}", f"{int(rank)}º")

    with c5:
        tds = int(qb_data["TD"].sum())
        rank = calculate_position(season_df, selected_qb, "TD")
        if rank >= 16:
            st.metric("Touchdowns", tds, f"{(-int(rank))}º")
        else:
            st.metric("Touchdowns", tds, f"{int(rank)}º")

    with c6:
        ints = int(qb_data["Int"].sum())
        rank = calculate_position(season_df, selected_qb, "Int")
        if rank <= 16:
            st.metric("Intercepciones", ints, f"{(-int(rank))}º")
        else:    
            st.metric("Intercepciones", ints, f"{int(rank)}º")

    with c7:
        rating = float(qb_data['Rate'].iloc[0])
        rank = calculate_position(season_df, selected_qb, "Rate")
        if rank >= 16:
            st.metric('Rating', value=round(rating, 2), delta=f"{(-int(rank))}º")
        else:
            st.metric('Rating', value=round(rating, 2), delta=f"{int(rank)}º")

    with c8:
        qb_rank = calculate_qb_rank(season_df, selected_qb)
        st.metric("Rk de QB", f"{qb_rank}º")
    