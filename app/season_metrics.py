# app/season_metrics.py
import streamlit as st
import pandas as pd
from helpers.data_filter import team_for_season

def calculate_position(df, player, metric):
    df = df[df["Att"] > 110]
    df = df.sort_values(by=metric, ascending=False).reset_index(drop=True)
    df[metric + "_rank"] = df[metric].rank(method="min", ascending=False)
    return df.loc[df["Player"] == player, metric + "_rank"].values[0]

def calculate_defense_position(df, team_name, metric):

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
    df = df.copy()

    # Obtener el nombre completo del equipo
    team_full_name = team_for_season(player, qb_data, season)
    if not team_full_name:
        return None  # Si no encuentra el equipo, devolver None

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

def rank_in_stat(qb_data,all_qb_in_season, selected_qb, stat):
    if stat == 'Cmp%' or stat == 'Rate':
        stat_value = float(qb_data[stat].iloc[0])
    else:
        stat_value = int(qb_data[stat].sum())

    titulos = {
        'Att':'Atts',
        'Cmp%':'Cmp%',
        'Yds': 'Air Yds',
        'Y/G':'Yds por juego',
        'TD':'Touchdowns',
        'Int':'Ints',
        'Rate':'Rating'
    }

    rank = calculate_position(all_qb_in_season, selected_qb, stat)
    if stat == 'Int':
        if rank > 20:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(rank))}º",border=True)
        elif rank > 10:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º", "off",border=True)
        else:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º","inverse",border=True)
    else:
        if rank > 20:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(rank))}º","inverse",border=True)
        elif rank > 10:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º", "off",border=True)
        else:
            st.metric(titulos[stat], f"{stat_value:,}", f"{int(rank)}º",border=True)

def defense_rank_in_stat(qb_defense_in_season,season_defense,team_name, stat):
    if stat == 'Y/P':
        stat_value = float(qb_defense_in_season[stat].iloc[0])
    else:
        stat_value = int(qb_defense_in_season[stat].sum())

    titulos = {
        'Rushing Yds':'Rushing Yds',
        'Passing Yds':'Passing Yds',
        'Y/P': 'Yds por jugada',
        'PA':'Pts permitidos',
        'Passing TD':'Pases de TD',
        'Rushing TD':'Acarreos TD',
        'TO':'Robos de balón'
    }

    rank = calculate_defense_position(season_defense,team_name,stat)
    if stat == 'TO':
        if rank > 20:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(33-rank))}º",border=True)
        elif rank > 10:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(33-rank))}º", "off",border=True)
        else:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(33-rank))}º","inverse",border=True)
    else:
        if rank > 20:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(rank))}º","inverse",border=True)
        elif rank > 10:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(rank))}º", "off",border=True)
        else:
            st.metric(titulos[stat], f"{stat_value:,}", f"{(int(rank))}º",border=True)

def render_season_metrics(qb_data, qb_df, selected_season, selected_qb, season_defense):
    if selected_season == "Toda la carrera":
        all_qb_in_season = qb_df.groupby("Player").sum(numeric_only=True).reset_index()
    else:
        all_qb_in_season = qb_df[qb_df["Season"] == selected_season]
        team_name = team_for_season(selected_qb, qb_data, selected_season)
        qb_defense_in_season = season_defense[season_defense['Team'] == team_name]

    st.subheader(f'Estadisticas de {selected_qb} en {selected_season} con {team_name}')

    # Mostrar estadísticas de la temporada
    stats = ["Att", "Cmp%", "Yds", "Y/G", "TD", "Int", "Rate"]
    columns = st.columns(len(stats))

    for col, stat in zip(columns, stats):
        with col:
            rank_in_stat(qb_data, all_qb_in_season, selected_qb, stat)

    st.subheader(f'Ranking de {selected_qb} VS Ranking de su defensa en {selected_season}')

    c1, c2, c3 = st.columns(3)

    with c1:
        qb_rank = calculate_qb_rank(all_qb_in_season, selected_qb)
        st.metric(f"Ranking de {selected_qb} en {selected_season}", f"{qb_rank}º",border=True)
        
    with c2:
        defense_rank = calculate_defense_rank(season_defense,selected_season,selected_qb,qb_data)
        st.metric(f"Ranking de la defensa de {team_name}", f"{defense_rank}º", border=True)
    
    with c3:
        record = (qb_data['QBrec'].iloc[0])

        if record[-1:] == '0':
            record = record[:-2]

        st.metric(f"Record de {team_name} con {selected_qb}", f"{record}",border=True)

    st.subheader(f'Estadisticas defensivas de {team_name} en {selected_season}')
    
    # Mostrar estadísticas defensivas de la temporada
    stats = ["Rushing Yds", "Passing Yds", "Y/P", "PA", "Passing TD", "Rushing TD", "TO"]
    columns = st.columns(len(stats))

    for col, stat in zip(columns, stats):
        with col:
            defense_rank_in_stat(qb_defense_in_season,season_defense,team_name, stat)