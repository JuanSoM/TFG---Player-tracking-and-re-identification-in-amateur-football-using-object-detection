#!/usr/bin/env python3
import argparse
import os
from collections import defaultdict

def procesar_fichero(ruta_entrada: str, ruta_salida: str):
    # Leemos todas las líneas
    with open(ruta_entrada, 'r', encoding='utf-8') as f:
        lines = [l.rstrip('\n') for l in f]

    # Agrupamos índices de línea por frame
    grupos = defaultdict(list)
    for idx, line in enumerate(lines):
        frame = line.split(',', 1)[0]
        grupos[frame].append(idx)

    # Copiamos la lista original para ir modificando
    salida = list(lines)

    # Para cada frame, contamos apariciones de ID=5 y sólo en la 2ª lo cambiamos
    for frame, indices in grupos.items():
        contador5 = 0
        for i in indices:
            partes = salida[i].split(',')
            if len(partes) > 1 and partes[1] == '4':
                contador5 += 1
                if contador5 == 2:
                    partes[1] = '14'
                    salida[i] = ','.join(partes)
                    break  # ya hemos cambiado la 2ª, salimos

    # Escribimos el resultado
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(salida))

if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description='Cambia la segunda aparición de ID=5 por 20 en cada frame.'
    )
    p.add_argument('input_file',
                   help='Ruta al fichero de entrada (p. ej. mot_corr10 - copia.txt)')
    p.add_argument('output_file', nargs='?',
                   help='(Opcional) Ruta al fichero de salida. Por defecto crea output.csv junto al input.')
    args = p.parse_args()

    entrada = args.input_file
    if args.output_file:
        salida = args.output_file
    else:
        base, _ = os.path.splitext(entrada)
        salida = base + '_modificado.txt'

    if not os.path.isfile(entrada):
        print(f"Error: no existe el fichero “{entrada}”")
        exit(1)

    procesar_fichero(entrada, salida)
    print(f"¡Hecho! Fichero generado: {salida}")
