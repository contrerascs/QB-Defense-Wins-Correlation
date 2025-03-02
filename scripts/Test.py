import pandas as pd  

# Cargar datasets  
qb_df = pd.read_csv("data/processed/qb_stats.csv")  
defense_df = pd.read_csv("data/processed/defense_stats.csv")  
kickers_df = pd.read_csv("data/processed/kickers_stats.csv")  

# Mostrar primeras filas  
print(qb_df.head())  
print(defense_df.head())  
print(kickers_df.head())  