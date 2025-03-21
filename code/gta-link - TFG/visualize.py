import os
import cv2
import numpy as np
import random
from tqdm import tqdm  # Importar tqdm para la barra de progreso

# Ruta base donde se encuentran los archivos de tracklets
tracklet_base_folder = r"C:\Users\jismbs\Documents\gta-link\DeepEIoU_SoccerNet_Split+Connect_eps0.6_minSamples10_K3_mergeDist0.4_spatial1.0"

# Ruta base donde están las imágenes
base_folder = r"C:\Users\jismbs\Documents\path\to\SoccerNet\tracking\test"
output_base_folder = os.path.join(base_folder, "tracked_output")
os.makedirs(output_base_folder, exist_ok=True)

# Leer los archivos de tracklets
detections = {}
colors = {}

# Para asegurarnos de que no procesamos el mismo archivo varias veces
processed_clips = set()

# Recorrer todas las carpetas dentro de base_folder
for root, dirs, files in os.walk(base_folder):
    # Buscamos la carpeta 'img1' en cada carpeta de clip
    if 'img1' in dirs:
        # Nombre de la subcarpeta (por ejemplo, SNMOT-116)
        clip_name = os.path.basename(root)
        
        # Asegurarse de no procesar el mismo clip más de una vez
        if clip_name in processed_clips:
            continue
        processed_clips.add(clip_name)
        
        # Construir la ruta al archivo de tracklet correspondiente a esta subcarpeta
        tracklet_file = os.path.join(tracklet_base_folder, f"{clip_name}.txt")
        
        # Verificar si el archivo de tracklets existe
        if not os.path.exists(tracklet_file):
            print(f"Tracklet file no encontrado: {tracklet_file}")
            continue
        
        # Leer el archivo de tracklets
        detections.clear()  # Limpiar las detecciones previas para este clip
        colors.clear()  # Limpiar los colores previos para este clip
        
        with open(tracklet_file, "r") as f:
            for line in f:
                frame_id, track_id, x, y, w, h, _, _, _, _ = map(float, line.strip().split(","))
                frame_id, track_id = int(frame_id), int(track_id)
                
                if track_id not in colors:
                    colors[track_id] = [random.randint(0, 255) for _ in range(3)]
                
                if frame_id not in detections:
                    detections[frame_id] = []
                detections[frame_id].append((track_id, int(x), int(y), int(w), int(h)))

        # Ruta de la carpeta con las imágenes del clip
        image_folder = os.path.join(root, 'img1')
        output_folder = os.path.join(output_base_folder, os.path.relpath(image_folder, base_folder))
        os.makedirs(output_folder, exist_ok=True)

        # Usar tqdm para la barra de progreso sobre los frames
        for frame_id in tqdm(sorted(detections.keys()), desc=f"Procesando {clip_name}", ncols=100):
            img_path = os.path.join(image_folder, f"{frame_id:06d}.jpg")
            if not os.path.exists(img_path):
                continue
            
            img = cv2.imread(img_path)
            for track_id, x, y, w, h in detections[frame_id]:
                color = colors[track_id]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, str(track_id), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            output_path = os.path.join(output_folder, f"{frame_id:06d}.jpg")
            cv2.imwrite(output_path, img)

print("Procesamiento completado. Las imágenes están en:", output_base_folder)

#python visualize.py