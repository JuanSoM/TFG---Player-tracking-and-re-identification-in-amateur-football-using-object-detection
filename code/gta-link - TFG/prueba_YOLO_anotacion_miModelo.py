import os
from ultralytics import YOLO
import cv2
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


# 1. Cargar TU modelo personalizado (reemplaza la ruta)
model = YOLO("runs/detect/yolov8_handball4/weights/best.pt")  # <-- Usa tu modelo

# 2. Abrir video
video_path = "video2.mp4"
cap = cv2.VideoCapture(video_path)

# 3. Crear archivo de resultados
os.makedirs("gt", exist_ok=True)
output_txt = "gt/gt.txt"

frame_id = 0
with open(output_txt, "w") as f:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 4. Tracking con TU modelo (configuración mínima)
        results = model.track(frame, persist=True)  # Persistencia de IDs
        
        # 5. Escribir detecciones
        if results[0].boxes.id is not None:
            for box, track_id in zip(results[0].boxes.xyxy, results[0].boxes.id):
                x1, y1, x2, y2 = map(int, box)
                f.write(f"{frame_id+1},{int(track_id)},{x1},{y1},{x2-x1},{y2-y1},1,0,-1,-1\n")

        frame_id += 1

cap.release()
print(f"✅ Anotaciones guardadas en: {output_txt}")
#python prueba_YOLO_anotacion_miModelo.py
#python prueba_YOLO_anotacion_miModelo.py --video_path video1.mp4 --output_dir gt