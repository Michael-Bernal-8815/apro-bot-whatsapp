import csv
import os

def exportar_respuestas_csv(respuestas, numero):
    # Crear carpeta si no existe
    carpeta_resultados = os.path.join("data", "resultados")
    os.makedirs(carpeta_resultados, exist_ok=True)

    filename = os.path.join(carpeta_resultados, "resultados_encuesta.csv")
    existe = os.path.isfile(filename)

    # Fila a exportar
    fila = [numero] + [r["respuesta"] for r in respuestas]

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        if not existe:
            encabezado = ["numero"] + [f"respuesta_{i+1}" for i in range(len(respuestas))]
            writer.writerow(encabezado)

        writer.writerow(fila)
