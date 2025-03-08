import re
from helpers.data_loader import load_datasets
from helpers.data_utils import TEAM_NAMES

# Cargar datasets una sola vez
qb_df,_,_ = load_datasets()
qb_df['Awards'] = qb_df['Awards'].fillna('')

def extract_awards(player_name):
    # Filtrar las filas correspondientes al jugador
    player_rows = qb_df[qb_df['Player'] == player_name]
    
    if player_rows.empty:
        return f"No se encontraron datos para {player_name}"
    
    # Inicializar contadores
    awards_totals = {
        'MVP': 0,
        'First Team All-Pro': 0,
        'Second Team All-Pro': 0,
        'Ofensive Player Of The Year': 0,
        'Ofensive Rockie Of The Year': 0,
        'Comback Player Of The Year': 0
    }
    
    # Función para contar premios en una temporada
    def count_awards(awards_str):
        return {
            'MVP': len(re.findall(r'MVP-1AP', awards_str)),
            'First Team All-Pro': len(re.findall(r'PBAP-1AP', awards_str)),
            'Second Team All-Pro': len(re.findall(r'PBAP-2AP', awards_str)),
            'Ofensive Player Of The Year': len(re.findall(r'OPoY-[1]', awards_str)),
            'Ofensive Rockie Of The Year': len(re.findall(r'ORoY-[1]', awards_str)),
            'Comback Player Of The Year': len(re.findall(r'CPoY-[1]', awards_str))
        }
    
    # Recorrer las filas del jugador y sumar los premios
    for awards_str in player_rows['Awards']:
        awards_count = count_awards(awards_str)
        for key in awards_totals:
            awards_totals[key] += awards_count[key]
    
    return awards_totals

def teams(player_name, qb_data):
    # Filtrar dataset para obtener las temporadas del QB seleccionado
    qb_seasons = qb_data[qb_data["Player-additional"] == player_name]
    seasons = qb_seasons['Season'].min()
    if seasons <= 1996:
        TEAM_NAMES['HOU'] = 'Houston Oilers'

    # Obtener los equipos únicos en los que ha jugado el QB
    qb_teams_abbr = qb_seasons["Team"].unique()

    # Convertir abreviaciones a nombres completos
    qb_teams_full = [TEAM_NAMES[abbr] for abbr in qb_teams_abbr if abbr in TEAM_NAMES]

    return qb_teams_full

def team_for_season(player_name, qb_data, season):
    if season <= 1996:
        TEAM_NAMES['HOU'] = 'Houston Oilers'

    # Filtrar dataset para obtener las temporadas del QB seleccionado y para la temporada específica
    qb_season_data = qb_data[(qb_data["Player"] == player_name) & (qb_data["Season"] == season)]

    # Verificar si existe información para esa temporada
    if qb_season_data.empty:
        return f"No se encontraron datos para {player_name} en la temporada {season}"

    # Obtener el equipo correspondiente para esa temporada
    team_abbr = qb_season_data["Team"].values[0]

    # Convertir abreviación a nombre completo del equipo
    team_full_name = TEAM_NAMES.get(team_abbr, 'Equipo desconocido')

    return team_full_name