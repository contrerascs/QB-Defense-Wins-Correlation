import csv
def clean_data(year):
    # Ruta del archivo de texto
    input_file = f'nfl_passing_{year}.txt'
    output_file = f'data/nfl_passing_{year}.csv'

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

for year in range(1985,2025):
    clean_data(year)
