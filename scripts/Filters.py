import pandas as pd
import re

# Cargar el dataset
df = pd.read_csv('data/processed/qb_stats.csv')

df['Awards'] = df['Awards'].fillna('')

def extract_awards(player_name):
    # Filtrar las filas correspondientes al jugador
    player_rows = df[df['Player'] == player_name]
    
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
    # Diccionario de equipos
    team_names = {
        'ARI': 'Arizona Cardinals', 'ATL': 'Atlanta Falcons', 'BAL': 'Baltimore Ravens',
        'BUF': 'Buffalo Bills', 'CAR': 'Carolina Panthers', 'CHI': 'Chicago Bears',
        'CIN': 'Cincinnati Bengals', 'CLE': 'Cleveland Browns', 'DAL': 'Dallas Cowboys',
        'DEN': 'Denver Broncos', 'DET': 'Detroit Lions', 'GB': 'Green Bay Packers',
        'HOU': 'Houston Texans', 'IND': 'Indianapolis Colts', 'JAX': 'Jacksonville Jaguars',
        'KAN': 'Kansas City Chiefs', 'LVR': 'Las Vegas Raiders', 'LAC': 'Los Angeles Chargers',
        'LAR': 'Los Angeles Rams', 'MIA': 'Miami Dolphins', 'MIN': 'Minnesota Vikings',
        'NWE': 'New England Patriots', 'NOR': 'New Orleans Saints', 'NYG': 'New York Giants',
        'NYJ': 'New York Jets', 'PHI': 'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers',
        'SFO': 'San Francisco 49ers', 'SEA': 'Seattle Seahawks', 'TAM': 'Tampa Bay Buccaneers',
        'TEN': 'Tennessee Titans', 'WAS': 'Washington Commanders' , 'STL': 'St. Louis Rams','RAI':'Los Angeles Raiders',
        'RAM': 'Los Angeles Rams', 'SDG': 'San Diego Chargers'
    }

    # Filtrar dataset para obtener las temporadas del QB seleccionado
    qb_seasons = qb_data[qb_data["Player-additional"] == player_name]

    # Obtener los equipos únicos en los que ha jugado el QB
    qb_teams_abbr = qb_seasons["Team"].unique()

    # Convertir abreviaciones a nombres completos
    qb_teams_full = [team_names[abbr] for abbr in qb_teams_abbr if abbr in team_names]

    return qb_teams_full