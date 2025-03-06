# app/metrics.py
import streamlit as st
import pandas as pd
from scripts.Filters import teams
from scripts.Filters import team_for_season

def calculate_position(df, player, metric):
    df = df[df["Att"] > 110]
    df = df.sort_values(by=metric, ascending=False).reset_index(drop=True)
    df[metric + "_rank"] = df[metric].rank(method="min", ascending=False)
    return df.loc[df["Player"] == player, metric + "_rank"].values[0]

def calculate_defense_position(df, player, qb_data, selected_season, metric):
    team_name = team_for_season(player, qb_data, selected_season)

    if team_name is None or team_name not in df["Team"].values:
        return None  # Evitar errores si el equipo no está

    df = df.sort_values(by=metric, ascending=False).reset_index(drop=True)
    df[metric + "_rank"] = df[metric].rank(method="min", ascending=False)

    # Obtener ranking de la defensa
    rank_values = df.loc[df["Team"] == team_name, metric + "_rank"].values
    return 33 - (rank_values[0] if len(rank_values) > 0 else None)

def calculate_qb_rank(df, player):
    # Excluir jugadores con pocos intentos para evitar sesgos
    df = df[df["Att"] > 110].copy()

    # Normalización de métricas
    df["Yds_norm"] = df["Yds"] / df["Yds"].max()
    df["TD_norm"] = df["TD"] / df["TD"].max()
    df["TD%_norm"] = df["TD%"] / df["TD%"].max()
    df["Rate_norm"] = df["Rate"] / df["Rate"].max()
    df["Y/A_norm"] = df["Y/A"] / df["Y/A"].max()

    df["Int_norm"] = df["Int"] / df["Int"].max()
    df["Sk%_norm"] = df["Sk%"] / df["Sk%"].max()

    # Puntaje final con ponderaciones
    df["QB_Score"] = (
        (df["Yds_norm"] * 1.5) +
        (df["TD_norm"] * 2) +
        (df["TD%_norm"] * 1.5) +
        (df["Rate_norm"] * 2) +
        (df["Y/A_norm"] * 1.2) -
        (df["Int_norm"] * 2) -
        (df["Sk%_norm"] * 1)
    )

    # Ordenamos y asignamos ranking
    df = df.sort_values(by="QB_Score", ascending=False).reset_index(drop=True)
    df["QB_Rank"] = df.index + 1

    # Devolver ranking del jugador específico
    rank = df.loc[df["Player"] == player, "QB_Rank"].values
    return int(rank[0]) if len(rank) > 0 else None

def calculate_defense_rank(df, season, player, qb_data):
    # Obtener el nombre completo del equipo
    team_full_name = team_for_season(player, qb_data, season)
    print(team_full_name)
    if not team_full_name:
        return None  # Si no encuentra el equipo, devolver None

    # Filtrar por la temporada específica
    df = df[df["Season"] == season].copy()

    # Normalización de métricas
    df["PA_norm"] = df["PA"] / df["PA"].max()
    df["Total Yds_norm"] = df["Total Yds"] / df["Total Yds"].max()
    df["Y/P_norm"] = df["Y/P"] / df["Y/P"].max()
    df["Passing Yds_norm"] = df["Passing Yds"] / df["Passing Yds"].max()
    df["Rushing Yds_norm"] = df["Rushing Yds"] / df["Rushing Yds"].max()
    df["Sc%_norm"] = df["Sc%"] / df["Sc%"].max()
    df["Exp_norm"] = df["EXP"] / df["EXP"].max()

    df["TO_norm"] = df["TO"] / df["TO"].max()
    df["Int_norm"] = df["Int"] / df["Int"].max()
    df["FL_norm"] = df["FL"] / df["FL"].max()
    df["TO%_norm"] = df["TO%"] / df["TO%"].max()

    # Ponderación para calcular la puntuación final de la defensa
    df["Defense_Score"] = (
        (-(df["TO_norm"] * 1.5)) +  # Reducido un poco
        (df["Int_norm"] * 2) +  # Aumentado el peso a Intercepciones
        (df["FL_norm"] * 1.5) +  # Ajustado Fumbles
        (df["TO%_norm"] * 1.5) +  # Ajustado Turnover %
        (-(df["PA_norm"] * 3)) +  # Aumentado el peso a PA
        (-(df["Total Yds_norm"] * 2.5)) +  # Aumentado el peso a Total Yds
        (-(df["Y/P_norm"] * 1.5)) +  # Mantenido Yardas por pase
        (-(df["Passing Yds_norm"] * 1.5)) +  # Mantenido Yardas por pase
        (-(df["Rushing Yds_norm"] * 1.5)) +  # Mantenido Yardas por carrera
        (-(df["Sc%_norm"] * 2)) +  # Mantenido porcentaje de anotación
        ((df["Exp_norm"] * 3))  # Reducido el peso de la experiencia
    )

    # Ordenar y asignar ranking
    df = df.sort_values(by="Defense_Score", ascending=False).reset_index(drop=True)
    df["Defense_Rank"] = df.index + 1

    # Devolver ranking del equipo en esa temporada
    rank = df.loc[df["Team"] == team_full_name, "Defense_Rank"].values
    return int(rank[0]) if len(rank) > 0 else None


def render_season_metrics(qb_data, qb_df, selected_season, selected_qb, defense_df):
    if selected_season == "Toda la carrera":
        season_df = qb_df.groupby("Player").sum(numeric_only=True).reset_index()
    else:
        season_df = qb_df[qb_df["Season"] == selected_season]
        season_defense = defense_df[defense_df["Season"] == selected_season]
        qb_defense = season_defense[season_defense['Team'] == team_for_season(selected_qb,qb_data,selected_season)]
        print(qb_defense.head())

    st.subheader(f'Estadisticas de {selected_qb} en {selected_season}')

    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    with c4:
        ypg = int(qb_data["Y/G"].sum())
        rank = calculate_position(season_df, selected_qb, "Y/G")
        print(rank)
        if rank > 20:
            st.metric("Y/G", f"{ypg:,}", f"{(int(rank))}º","inverse",border=True)
        elif rank > 10:
            st.metric("Y/G", f"{ypg:,}", f"{int(rank)}º", "off",border=True)
        else:
            st.metric("Y/G", f"{ypg:,}", f"{int(rank)}º",border=True)

    with c1:
        atts = int(qb_data["Att"].sum())
        rank = calculate_position(season_df, selected_qb, "Att")
        print(rank)
        if rank > 20:
            st.metric("Atts", f"{atts:,}", f"{(int(rank))}º","inverse",border=True)
        elif rank > 10:
            st.metric("Atts", f"{atts:,}", f"{int(rank)}º", "off",border=True)
        else:
            st.metric("Atts", f"{atts:,}", f"{int(rank)}º",border=True)

    with c2:
        cmp_value = float(qb_data['Cmp%'].iloc[0])
        rank = calculate_position(season_df, selected_qb, "Cmp%")
        if rank > 20:
            st.metric('Cmp%', f"{round(cmp_value, 1)}%", f"{(-int(rank))}º",'inverse',border=True)
        elif rank > 10:
            st.metric('Cmp%', f"{round(cmp_value, 1)}%", f"{(int(rank))}º","off",border=True)
        else:
            st.metric('Cmp%', f"{round(cmp_value, 1)}%", f"{int(rank)}º",border=True)

    with c3:
        yards = int(qb_data["Yds"].sum())
        rank = calculate_position(season_df, selected_qb, "Yds")
        if rank > 20:
            st.metric("Total Yds", f"{yards:,}", f"{(int(rank))}º",'inverse',border=True)
        elif rank > 10:
            st.metric("Total Yds", f"{yards:,}", f"{(int(rank))}º",'off',border=True)
        else:
            st.metric("Total Yds", f"{yards:,}", f"{int(rank)}º",border=True)

    with c5:
        tds = int(qb_data["TD"].sum())
        rank = calculate_position(season_df, selected_qb, "TD")
        if rank > 20:
            st.metric("Touchdowns", tds, f"{(-int(rank))}º",'inverse',border=True)
        elif rank > 10:
            st.metric("Touchdowns", tds, f"{(-int(rank))}º",'off',border=True)
        else:
            st.metric("Touchdowns", tds, f"{int(rank)}º",border=True)

    with c6:
        ints = int(qb_data["Int"].sum())
        rank = calculate_position(season_df, selected_qb, "Int")
        if rank > 20:
            st.metric("Ints", ints, f"{(-int(rank))}º",'inverse',border=True)
        elif rank > 10:
            st.metric("Ints", ints, f"{(-int(rank))}º",'off',border=True)
        else:    
            st.metric("Ints", ints, f"{int(rank)}º",border=True)

    with c7:
        rating = float(qb_data['Rate'].iloc[0])
        rank = calculate_position(season_df, selected_qb, "Rate")
        if rank > 20:
            st.metric('Rating', round(rating, 2), f"{(-int(rank))}º",'inverse',border=True)
        elif rank > 10:
            st.metric('Rating', round(rating, 2), f"{(-int(rank))}º",'off',border=True)
        else:
            st.metric('Rating', round(rating, 2), f"{int(rank)}º",border=True)

    #with c8:
    #    qb_rank = calculate_qb_rank(season_df, selected_qb)
    #    st.metric("Rk de QB", f"{qb_rank}º",border=True)
        #print(calculate_defense_rank(defense_df,selected_season,selected_qb,qb_data))

    st.subheader(f'Estadisticas defensivas de {team_for_season(selected_qb,qb_data,selected_season)} en {selected_season}')
    
    # Metrícas Defensivas en la temporada
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

    with c1:
        atts = int(qb_defense["Rushing Yds"].sum())
        defense_rank = calculate_defense_position(season_defense,selected_qb,qb_data,selected_season, "Rushing Yds")
        if defense_rank > 20:
            st.metric("Rushing Yds", f"{atts:,}", f"{(-int(defense_rank))}º",border=True)
        elif defense_rank > 10:
            st.metric("Rushing Yds", f"{atts:,}", f"{(-int(defense_rank))}º", "off",border=True)
        else:
            st.metric("Rushing Yds", f"{atts:,}", f"{(-int(defense_rank))}º","inverse",border=True)

    with c2:
        atts = int(qb_defense["Passing Yds"].sum())
        defense_rank = calculate_defense_position(season_defense,selected_qb,qb_data,selected_season, "Passing Yds")
        if defense_rank > 20:
            st.metric("Passing Yds", f"{atts:,}", f"{(-int(defense_rank))}º",border=True)
        elif defense_rank > 10:
            st.metric("Passing Yds", f"{atts:,}", f"{(-int(defense_rank))}º", "off",border=True)
        else:
            st.metric("Passing Yds", f"{atts:,}", f"{(-int(defense_rank))}º","inverse",border=True)

    with c3:
        cmp_value = float(qb_defense['Y/P'].iloc[0])
        defense_rank = calculate_defense_position(season_defense,selected_qb,qb_data,selected_season,'Y/P')
        if defense_rank > 20:
            st.metric('Yardas por jugada', f"{cmp_value}", f"{(-int(defense_rank))}º", border=True)
        elif defense_rank > 10:
            st.metric('Yardas por jugada', f"{cmp_value}", f"{(-int(defense_rank))}º",'off', border=True)
        else:
            st.metric('Yardas por jugada', f"{cmp_value}", f"{(-int(defense_rank))}º",'inverse', border=True)

    with c4:
        ppa = int(qb_defense["PA"].sum())
        defense_rank = calculate_defense_position(season_defense,selected_qb,qb_data,selected_season,'PA')
        if defense_rank > 20:
            st.metric("Puntos permitidos", f"{ppa:,}", f"{(-int(defense_rank))}º", border=True)
        elif defense_rank > 10:
            st.metric("Puntos permitidos", f"{ppa:,}", f"{(-int(defense_rank))}º",'off', border=True)
        else:
            st.metric("Puntos permitidos", f"{ppa:,}", f"{(-int(defense_rank))}º",'inverse',border=True)

    with c5:
        tds = int(qb_defense["Passing TD"].sum())
        defense_rank = calculate_defense_position(season_defense,selected_qb,qb_data,selected_season,'Passing TD')
        if defense_rank > 20:
            st.metric("Pases de TD", tds, f"{(-int(defense_rank))}º", border=True)
        elif defense_rank > 10:
            st.metric("Pases de TD", tds, f"{(-int(defense_rank))}º",'off', border=True)            
        else:
            st.metric("Pases de TD", tds, f"{(-int(defense_rank))}º",'inverse', border=True)

    with c6:
        tds = int(qb_defense["Rushing TD"].sum())
        defense_rank = calculate_defense_position(season_defense,selected_qb,qb_data,selected_season,'Rushing TD')
        if defense_rank > 20:
            st.metric("Accarreos de TD", tds, f"{(-int(defense_rank))}º", border=True)
        elif defense_rank > 10:
            st.metric("Accarreos de TD", tds, f"{(-int(defense_rank))}º",'off',border=True)
        else:
            st.metric("Accarreos de TD", tds, f"{(-int(defense_rank))}º",'inverse',border=True)

    with c7:
        to = int(qb_defense["TO"].sum())
        defense_rank = calculate_defense_position(season_defense,selected_qb,qb_data,selected_season,'TO')
        if defense_rank > 20:
            st.metric("Robos de balón", to, f"{(int(33-defense_rank))}º", border=True)
        elif defense_rank > 10:
            st.metric("Robos de balón", to, f"{(int(33-defense_rank))}º",'off', border=True)
        else:
            st.metric("Robos de balón", to, f"{(int(33-defense_rank))}º",'inverse', border=True)

    #with c8:
    #    defense_rank = calculate_defense_rank(defense_df,selected_season,selected_qb,qb_data)
    #    st.metric("Rk de Defensa", f"{defense_rank}º")
