import os
import cv2
import random
from tqdm import tqdm

# Configuración de rutas
#tracklet_file = r"C:\Users\jismbs\Documents\gta-link\DeepEIoU_SoccerNet_Split+Connect_eps0.8_minSamples10_K4_mergeDist0.7_spatial1.0\video2.txt" #DeepEIoU_frames_football_Split+Connect_eps0.6_minSamples10_K3_mergeDist0.4_spatial1.0\video2.txt
tracklet_file = r"C:\Users\jismbs\Documents\gta-link\DeepEIoU_SoccerNet_Split+Connect_eps0.8_minSamples10_K4_mergeDist0.7_spatial1.0\video2_mydata.txt"
image_folder = r"C:\Users\jismbs\Documents\gta-link\frames_trackerVideo2DeepEIoU_osnet_ImageNet_Soccernet\video2\img1"
#output_folder = r"C:\Users\jismbs\Documents\gta-link\tracked_output_DeepEIoU_trackerVideo2_HiperparametersOptimized_SinCorreccion" #C:\Users\jismbs\Documents\gta-link\tracked_output_DeepEIoU_trackerVideo2_HiperparametersOptimized
output_folder = r"C:\Users\jismbs\Documents\gta-link\osnetMyData+gta_link"
   

os.makedirs(output_folder, exist_ok=True)

# 1. Cargar tracklets (convertir valores decimales a enteros)
print("Cargando datos de tracklets...")
detections = {}
colors = {}

with open(tracklet_file, 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        try:
            # Convertir a float primero y luego a int para manejar valores como "1.0"
            frame_id = int(float(parts[0]))
            track_id = int(float(parts[1]))
            x, y, w, h = map(float, parts[2:6])
            
            if track_id not in colors:
                colors[track_id] = (
                    random.randint(50, 200),
                    random.randint(50, 200),
                    random.randint(50, 200)
                )
            
            if frame_id not in detections:
                detections[frame_id] = []
            detections[frame_id].append((track_id, int(x), int(y), int(w), int(h)))
        except (ValueError, IndexError) as e:
            print(f"Advertencia: Error al procesar línea - {line.strip()}. Error: {e}")
            continue

# 2. Procesar frames
print("\nGenerando visualizaciones...")
for frame_id in tqdm(sorted(detections.keys()), desc="Procesando frames"):
    img_path = os.path.join(image_folder, f"{frame_id:06d}.jpg")
    if not os.path.exists(img_path):
        continue
    
    img = cv2.imread(img_path)
    
    for track_id, x, y, w, h in detections[frame_id]:
        color = colors[track_id]
        
        # Bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        
        # Etiqueta con ID
        label = f"ID:{track_id}"
        (text_width, text_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, (x, y - text_height - 10), (x + text_width, y), color, -1)
        cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)
    
    cv2.imwrite(os.path.join(output_folder, f"{frame_id:06d}.jpg"), img)

print(f"\nVisualización completada. Resultados en:\n{output_folder}")