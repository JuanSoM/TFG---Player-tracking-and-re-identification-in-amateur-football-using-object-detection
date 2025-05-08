import os
import cv2

def extract_frames(video_path, output_dir):
    """
    Extrae los frames de un video y los guarda en la estructura MOT Challenge.
    
    Args:
        video_path (str): Ruta al video de entrada (ej: 'video1.mp4').
        output_dir (str): Directorio base de salida (ej: 'frames/').
    """
    # Crear estructura de directorios (MOT Challenge style)
    seq_name = os.path.splitext(os.path.basename(video_path))[0]  # 'video1' si el input es 'video1.mp4'
    img_dir = os.path.join(output_dir, seq_name, "img1")
    os.makedirs(img_dir, exist_ok=True)
    
    # Abrir video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"No se pudo abrir el video: {video_path}")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        frame_filename = f"{frame_count:06d}.jpg"  # Formato: 000001.jpg, 000002.jpg, ...
        frame_path = os.path.join(img_dir, frame_filename)
        cv2.imwrite(frame_path, frame)
    
    cap.release()
    print(f"✅ {frame_count} frames extraídos y guardados en: {img_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extrae frames de un video y los guarda en estructura MOT Challenge.")
    parser.add_argument("--video_path", type=str, required=True, help="Ruta al video de entrada (ej: 'video1.mp4').")
    parser.add_argument("--output_dir", type=str, default="frames", help="Directorio base de salida (ej: 'frames/').")
    args = parser.parse_args()
    
    extract_frames(args.video_path, args.output_dir)


#prueba de extracción de frames
#python extract_frames.py --video_path video1.mp4 --output_dir frames