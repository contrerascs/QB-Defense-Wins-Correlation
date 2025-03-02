import csv
import os
import pandas as pd

def clean_qb_data(year):
    # Ruta del archivo de texto
    input_file = f'data_txt/passing_stats/nfl_passing_{year}.txt'
    output_file = f'data/qbs/qb_stats_{year}.csv'

    # Frase que necesitamos eliminar
    phrase_to_remove = '--- When using SR data, please cite us and provide a link and/or a mention.'

    # Abrimos el archivo de entrada
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Eliminar las primeras líneas en blanco y la frase específica
    cleaned_lines = []
    found_phrase = False  # Para saber si encontramos la frase a eliminar

    for line in lines:
        # Si encontramos la frase a eliminar, la saltamos
        if not found_phrase and line.strip() == phrase_to_remove:
            found_phrase = True
            continue
        # Eliminamos líneas vacías, solo si ya encontramos la frase
        if line.strip() or found_phrase:
            cleaned_lines.append(line)

    # Procesamos el contenido limpio para convertirlo a formato CSV
    csv_data = []

    # Convertimos cada línea en una lista separada por comas (como un CSV)
    for line in cleaned_lines:
        # Si la línea no está vacía, la dividimos por las comas
        if line.strip():
            csv_data.append(line.strip().split(','))

    # Guardamos los datos procesados en un archivo CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)

    print(f"Archivo CSV limpio guardado como {output_file}")

def clean_defense_data(year):
    import pandas as pd

    # Cargar el archivo TXT
    with open(f"data_txt/defense_stats/nfl_defense_{year}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Eliminar la primera línea (frase que no sirve)
    lines = lines[1:]

    # Eliminar líneas vacías
    lines = [line.strip() for line in lines if line.strip()]

    # Eliminar la fila de títulos de sección (detectamos si empieza con ",,,," porque no tiene datos numéricos)
    lines = [line for line in lines if not line.startswith(",,,,")]

    # Convertir las líneas en un DataFrame
    data = [line.split(",") for line in lines]
    df = pd.DataFrame(data)

    # Asignar nombres de columnas corregidos
    if year >= 2000:
        column_names = [
        "Rk", "Tm", "G", "PA", "Total Yds", "Ply", "Y/P", "TO", "FL", "Total 1stD",
        "Cmp", "Passing Att", "Passing Yds", "Passing TD", "Int", "NY/A", "Passing 1stD",
        "Rushing Att", "Rushing Yds", "Rushing TD", "Y/A", "Rushing 1stD",
        "Pen", "Penalties Yds", "1stPy", "Sc%", "TO%",'EXP'
        ]
    else:
        column_names = [
            "Rk", "Tm", "G", "PA", "Total Yds", "Ply", "Y/P", "TO", "FL", "Total 1stD",
            "Cmp", "Passing Att", "Passing Yds", "Passing TD", "Int", "NY/A", "Passing 1stD",
            "Rushing Att", "Rushing Yds", "Rushing TD", "Y/A", "Rushing 1stD",
            "Pen", "Penalties Yds", "1stPy", "Sc%", "TO%"
        ]

    df.columns = column_names

    # Eliminar las últimas 3 filas que contienen promedios y totales de la liga
    df = df.iloc[:-3]

    # Guardar en CSV
    df.to_csv(f"data/defense/defense_stats_{year}.csv", index=False, encoding="utf-8")

    print(f"Proceso completado. Archivo 'Defense_Stats_{year}.csv' generado correctamente.")

def custom_defense_data(year):
    data = pd.read_csv(f'data/defense/defense_stats_{year}.csv')
    
    # Eliminar la fila 2 (índice 1) sin verificar su contenido
    data = data.drop(index=0).reset_index(drop=True)

    # Eliminar la columna 'Rk' si existe
    if 'Rk' in data.columns:
        data = data.drop(columns=['Rk'])

    if year < 2000:
        # Agregar la nueva columna con el valor predeterminado
        data['EXP'] = 0
        data['Sc%'] = 0
        data['TO%'] = 0
        print(f"Columna 'EXP' agregada con éxito al archivo data/defense/defense_stats_{year}.csv")

    # Guardar el archivo actualizado (opcional)
    data.to_csv(f'data/defense/defense_stats_{year}.csv', index=False)
    print(f"Datos finales guardados en 'data/defense/defense_stats_{year}.csv'")

def custom_qb_data(year):
    data = pd.read_csv(f'data/qbs/qb_stats_{year}.csv')

    # Eliminar la columna 'Rk' si existe
    if 'Rk' in data.columns:
        data = data.drop(columns=['Rk'])

    if year < 2006:
        # Agregar la nueva columna con el valor predeterminado
        data['QBR'] = 0
        print(f"Columnas 'QBR' agregada con éxito al archivo data/defense/defense_stats_{year}.csv")
        if year < 1994:
            data['1D'] = 0
            data['Succ%'] = 0
            print(f"Columnas '1D','Succ%' agregada con éxito al archivo data/defense/defense_stats_{year}.csv")

    # Guardar el archivo actualizado (opcional)
    data.to_csv(f'data/qbs/qb_stats_{year}.csv', index=False)
    print(f"Datos finales guardados en 'data/qbs/qb_stats_{year}.csv'")

def filter_qb(year):
    # Cargar el archivo CSV
    file_path = f'data/qbs/qb_stats_{year}.csv'
    df = pd.read_csv(file_path)

    # Filtrar solo jugadores con posición 'QB'
    df = df[df['Pos'] == 'QB']

    # Filtrar jugadores con al menos 1 partido iniciado (GS >= 1)
    df = df[df['GS'] >= 1]

    # Filtrar jugadores con 'QBrec' no vacío y distinto de '0-0-0'
    df = df[df['QBrec'].notna() & (df['QBrec'].str.strip() != '') & (df['QBrec'] != '0-0-0')]

    # Eliminar la última fila del DataFrame
    df = df[:-1]

    # Sobrescribir el archivo CSV con los datos filtrados
    df.to_csv(file_path, index=False)

    print("Archivo filtrado y sobrescrito exitosamente.")

def clean_kickers_data(year):
    # Cargar el archivo TXT
    with open(f"data_txt/kickers/kickers_stats_{year}.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Eliminar la primera línea si no es un encabezado útil
    lines = lines[1:]

    # Eliminar líneas vacías
    lines = [line.strip() for line in lines if line.strip()]

    # Eliminar filas de títulos de sección (si empiezan con ",,,," es porque no contienen datos útiles)
    lines = [line for line in lines if not line.startswith(",,,,")]

    # Asegurar que todas las filas tengan el mismo número de columnas
    max_cols = max(len(line.split(",")) for line in lines)
    data = [line.split(",") + [""] * (max_cols - len(line.split(","))) for line in lines]

    # Convertir a DataFrame
    df = pd.DataFrame(data)

    # Definir nombres de columnas
    column_names = [
        "Rk", "Player", "Age", "Team", "Pos", "G", "GS", 
        "FGA-0-19", "FGM-0-19", "FGA-20-29", "FGM-20-29", "FGA-30-39", "FGM-30-39", 
        "FGA-40-49", "FGM-40-49", "FGA-50+", "FGM-50+","TotalFGA", "TotalFGM", "Lng", "FG%", 
        "XPA", "XPM", "XP%","KO", "KOYds", "TB", "TB%", "KOAvg", "Awards", "Player-additional"
    ]
    
    # Truncar en caso de que haya más columnas de las esperadas
    df.columns = column_names[:df.shape[1]]

    # Eliminar columnas nuevas de 2024 que no existían en 1985
    df = df.drop(columns=["Rk", "KO", "KOYds", "TB", "TB%", "KOAvg"], errors='ignore')

    df = df.dropna(subset=["Pos", "TotalFGA"])  # Eliminar filas donde estas columnas estén vacías

    df["TotalFGA"] = pd.to_numeric(df["TotalFGA"], errors='coerce')

    # Filtrar solo jugadores con posición 'K'
    df = df[df["Pos"] == 'K']

    # Filtrar jugadores con al menos 10 intentos (TotalFGA >= 10)
    df = df[df["TotalFGA"] >= 10]

    # Eliminar la última fila del DataFrame (promedios de la liga)
    df = df[:-1]

    # Verificar estructura antes de guardar
    print(df.head())  

    # Guardar como CSV limpio
    df.to_csv(f'data/kickers/kickers_stats_{year}.csv', index=False, encoding="utf-8")

    print("Archivo TXT filtrado y sobrescrito exitosamente.")

def rename_defense(year):
    df = pd.read_csv(f'data/defense/defense_stats_{year}.csv')

    # Suponiendo que quieres renombrar la columna "antiguo_nombre" a "nuevo_nombre"
    df = df.rename(columns={'Tm': 'Team'})

    # Paso 3: Guardar el DataFrame con el nuevo nombre de columna en un nuevo archivo CSV
    df.to_csv(f'data/defense/defense_stats_{year}.csv', index=False)

def join_files_csv():
    # Ruta a la carpeta con los archivos CSV
    data_folder = 'data/kickers'

    # Lista para almacenar los DataFrames
    qb_dataframes = []

    # Recorrer todos los archivos de QB
    for filename in os.listdir(data_folder):
        if filename.startswith('kickers_stats_') and filename.endswith('.csv'):
            # Extraer el año del nombre del archivo
            year = int(filename.split('_')[2].split('.')[0])
            # Cargar el archivo CSV
            df = pd.read_csv(os.path.join(data_folder, filename))
            # Agregar una columna 'Season'
            df['Season'] = year
            #Eliminar columna 'Player-additional'
            if 'Player-additional' in df.columns:
                df = df.drop(columns=['Player-additional'])
            # Agregar el DataFrame a la lista
            qb_dataframes.append(df)

    # Unir todos los DataFrames en uno solo
    qb_consolidated = pd.concat(qb_dataframes, ignore_index=True)


    # Reemplazar "0" con NaN en columnas numéricas
    qb_consolidated.replace(0, float('nan'), inplace=True)

    # Convertir columnas numéricas
    qb_consolidated = qb_consolidated.apply(pd.to_numeric, errors='ignore')

    # Guardar el DataFrame consolidado en un nuevo archivo CSV
    qb_consolidated.to_csv('data/processed/kickers_stats.csv', index=False)