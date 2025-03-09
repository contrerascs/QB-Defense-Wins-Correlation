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
def normalize_stats(df, stats):
    if stats in df.columns:
        min_val = df[stats].min()
        max_val = df[stats].max()
        if max_val - min_val != 0:  # Evitar divisiones por cero
            return (df[stats] - min_val) / (max_val - min_val) * 100
        else:
            return 50  # Valor neutral si no hay variación
    return None

def normalize_stats_plots(df, stat, player, invert=False):
    if stat in df.columns:
        min_val = df[stat].min()
        max_val = df[stat].max()
        if max_val - min_val != 0:
            normalized = ((df.loc[df["Player"] == player, stat].values[0] - min_val) / (max_val - min_val)) * 100
            if stat == 'Int':
                invert = True
            return 100 - normalized if invert else normalized
        else:
            return 50  # Valor neutral si no hay variación
    return None

def normalize_stats_defense_plots(df, stat, team, invert=False):
    if stat in df.columns:
        min_val = df[stat].min()
        max_val = df[stat].max()
        if max_val - min_val != 0:
            normalized = ((df.loc[df["Team"] == team, stat].values[0] - min_val) / (max_val - min_val)) * 100
            if stat == 'Int':
                invert = True
            return 100 - normalized if invert else normalized
        else:
            return 50  # Valor neutral si no hay variación
    return None

# Función de normalización
def normalize(value, min_val, max_val, invert=False):
    if max_val - min_val == 0:
        return 50  # Valor neutro si no hay variación
    norm_value = (value - min_val) / (max_val - min_val) * 100
    return 100 - norm_value if invert else norm_value

def calculate_qb_metrics(df, player):
    """Calcula métricas personalizadas para un QB en una escala de 0 a 100."""
    
    # Filtrar las estadísticas del QB
    qb_stats = df[df["Player"] == player].iloc[0]

    # Obtener valores mínimos y máximos de cada estadística
    min_max_values = {stat: (df[stat].min(), df[stat].max()) for stat in df.columns if stat in ["Cmp%", "AY/A", "Y/A", "Rate", "Int%", "Int", "TD%", "TD", "Y/G", "Sk%", "Yds.1", "4QC", "GWD", "QBR"]}

    # Normalizar cada estadística antes de combinar
    cmp_norm = normalize(qb_stats["Cmp%"], *min_max_values["Cmp%"])
    aya_norm = normalize(qb_stats["AY/A"], *min_max_values["AY/A"])
    ya_norm = normalize(qb_stats["Y/A"], *min_max_values["Y/A"])
    rate_norm = normalize(qb_stats["Rate"], *min_max_values["Rate"])
    intp_norm = normalize(qb_stats["Int%"], *min_max_values["Int%"], invert=True)
    int_norm = normalize(qb_stats["Int"], *min_max_values["Int"], invert=True)
    tdp_norm = normalize(qb_stats["TD%"], *min_max_values["TD%"])
    td_norm = normalize(qb_stats["TD"], *min_max_values["TD"])
    yg_norm = normalize(qb_stats["Y/G"], *min_max_values["Y/G"])
    sk_norm = normalize(qb_stats["Sk%"], *min_max_values["Sk%"], invert=True)
    yds1_norm = normalize(qb_stats["Yds.1"], *min_max_values["Yds.1"], invert=True)
    qc_norm = normalize(qb_stats["4QC"], *min_max_values["4QC"])
    gwd_norm = normalize(qb_stats["GWD"], *min_max_values["GWD"])
    qbr_norm = normalize(qb_stats["QBR"], *min_max_values["QBR"])

    # Cálculo de métricas personalizadas
    metrics = {
        "Presición": (cmp_norm * 0.7) + (aya_norm * 0.3),
        "Eficiencia": (ya_norm * 0.6) + (rate_norm * 0.4),
        "Seguridad": (intp_norm * 0.6) + (int_norm * 0.4),
        "Producción": ((tdp_norm * 0.5) + (td_norm * 0.3) + (yg_norm * 0.2)) / (0.5 + 0.3 + 0.2),
        "Mobilidad": (sk_norm * 0.7) + (yds1_norm * 0.3),
        "Clutch": (qc_norm * 0.6) + (gwd_norm * 0.4),
        "Impacto": (qbr_norm * 0.5) + (rate_norm * 0.3) + (tdp_norm * 0.2)
    }

    return metrics