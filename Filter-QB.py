import csv

def filter_qb(year):
    # Ruta del archivo CSV de entrada
    input_file = f'data/nfl_passing_{year}.csv'
    output_file = f'data/QB_STATS{year}.csv'

    # Abrimos el archivo CSV de entrada
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        csv_data = list(reader)

    # Identificamos el índice de la columna 'Pos' (asumimos que es la columna con la etiqueta 'Pos')
    header = csv_data[0]
    pos_index = header.index('Pos')

    # Filtramos los jugadores que son 'QB'
    filtered_data = [header]  # Incluimos los encabezados

    # Añadimos solo las filas que contienen 'QB' en la columna 'Pos'
    for row in csv_data[1:]:
        if row[pos_index] == 'QB':
            filtered_data.append(row)

    # Guardamos los datos filtrados en un nuevo archivo CSV
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(filtered_data)

    print(f"Archivo CSV con solo QBs guardado como {output_file}")

for year in range(1985,2025):
    filter_qb(year)
