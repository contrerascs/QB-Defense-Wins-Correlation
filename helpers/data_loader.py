import pandas as pd

def load_datasets():
    qb_df = pd.read_csv('data/processed/qb_stats.csv')
    defense_df = pd.read_csv('data/processed/defense_stats.csv')
    kickers_df = pd.read_csv('data/processed/kickers_stats.csv')
    return qb_df, defense_df, kickers_df