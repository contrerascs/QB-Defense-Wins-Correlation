import os

# Constantes
TEAM_NAMES = {
    'ARI': 'Arizona Cardinals', 'ATL': 'Atlanta Falcons', 'BAL': 'Baltimore Ravens',
    'BUF': 'Buffalo Bills', 'CAR': 'Carolina Panthers', 'CHI': 'Chicago Bears',
    'CIN': 'Cincinnati Bengals', 'CLE': 'Cleveland Browns', 'DAL': 'Dallas Cowboys',
    'DEN': 'Denver Broncos', 'DET': 'Detroit Lions', 'GNB': 'Green Bay Packers',
    'HOU': 'Houston Texans', 'IND': 'Indianapolis Colts', 'JAX': 'Jacksonville Jaguars',
    'KAN': 'Kansas City Chiefs', 'LVR': 'Las Vegas Raiders', 'LAC': 'Los Angeles Chargers',
    'LAR': 'Los Angeles Rams', 'MIA': 'Miami Dolphins', 'MIN': 'Minnesota Vikings',
    'NWE': 'New England Patriots', 'NOR': 'New Orleans Saints', 'NYG': 'New York Giants',
    'NYJ': 'New York Jets', 'PHI': 'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers',
    'SFO': 'San Francisco 49ers', 'SEA': 'Seattle Seahawks', 'TAM': 'Tampa Bay Buccaneers',
    'TEN': 'Tennessee Titans', 'WAS': 'Washington Commanders', 'STL': 'St. Louis Rams',
    'RAI': 'Los Angeles Raiders', 'RAM': 'Los Angeles Rams', 'SDG': 'San Diego Chargers'
}

# Verificar existencia de imagen
def get_image_path(qb_id):
    image_path = os.path.join("data", "images", f"{qb_id}.jpg")
    return image_path if os.path.exists(image_path) else os.path.join("data", "images", "Not_found_image.jpg")

# Normalizar estadísticas
def normalize_stats(df, stats, player):
    normalized_stats = {}
    for stat in stats:
        if stat in df.columns:
            min_val = df[stat].min()
            max_val = df[stat].max()
            normalized_stats[stat] = ((df.loc[df["Player"] == player, stat].values[0] - min_val) / (max_val - min_val)) * 100
    return normalized_stats