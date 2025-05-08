import os
import cv2

def extract_frames(video_path, output_dir, interval_seconds=20):
    """
    Extrae 1 frame cada X segundos de un video y los guarda en estructura MOT Challenge.
    
    Args:
        video_path (str): Ruta al video de entrada (ej: 'video1.mp4').
        output_dir (str): Directorio base de salida (ej: 'frames/').
        interval_seconds (int): Intervalo entre frames en segundos (default: 20).
    """
    # Crear estructura de directorios
    seq_name = os.path.splitext(os.path.basename(video_path))[0]  # Ej: 'video1' para 'video1.mp4'
    img_dir = os.path.join(output_dir, seq_name, "img1")
    os.makedirs(img_dir, exist_ok=True)
    
    # Abrir video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"No se pudo abrir el video: {video_path}")
    
    # Obtener FPS y calcular intervalo en frames
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"📹 Video: {video_path}")
    print(f"📊 FPS: {fps:.2f} | Intervalo: {frame_interval} frames (cada {interval_seconds}s)")
    
    frame_count = 0
    saved_count = 0
    
    for i in range(0, total_frames, frame_interval):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if not ret:
            break
        
        saved_count += 1
        frame_filename = f"{saved_count:06d}.jpg"  # Formato: 000001.jpg, 000002.jpg, ...
        frame_path = os.path.join(img_dir, frame_filename)
        cv2.imwrite(frame_path, frame)
        
        # Mostrar progreso cada 10 frames guardados
        if saved_count % 10 == 0:
            print(f"⏳ Procesados {i}/{total_frames} frames del video...")
    
    cap.release()
    print(f"\n✅ {saved_count} frames extraídos (1 cada {interval_seconds}s) guardados en:\n{img_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extrae 1 frame cada X segundos de un video.")
    parser.add_argument("--video_path", type=str, required=True, help="Ruta al video de entrada (ej: 'video1.mp4').")
    parser.add_argument("--output_dir", type=str, default="frames", help="Directorio base de salida (ej: 'frames/').")
    parser.add_argument("--interval", type=int, default=20, help="Intervalo entre frames en segundos (default: 20).")
    args = parser.parse_args()
    
    extract_frames(args.video_path, args.output_dir, args.interval)
    
#python extract_frames_20seconds.py --video_path video.mp4 --output_dir frames_for_YOLO_training