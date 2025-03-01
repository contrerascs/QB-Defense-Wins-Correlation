import csv
import os
import pandas as pd

def clean_data(year):
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

def clean_defensive_data(year):
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

def custom_data(year):
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


for year in range(1985,2025):
    clean_data(year)
    custom_qb_data(year)
    #clean_defensive_data(year)
    #custom_data(year)
