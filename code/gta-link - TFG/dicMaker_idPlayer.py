import os 
import cv2
import argparse
from tqdm import tqdm

def parse_mot_file(mot_file_path):
    detections = {}
    with open(mot_file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 6:
                continue
            
            frame_id = int(float(parts[0]))
            track_id = int(float(parts[1]))
            x, y, w, h = map(float, parts[2:6])
            
            if frame_id not in detections:
                detections[frame_id] = []
            detections[frame_id].append((track_id, int(x), int(y), int(w), int(h)))
    
    return detections

def crop_and_save_detections(image_folder, detections, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    for frame_id in tqdm(sorted(detections.keys()), desc="Procesando frames"):
        img_path = os.path.join(image_folder, f"{frame_id:06d}.jpg")
        
        if not os.path.exists(img_path):
            continue
        
        img = cv2.imread(img_path)
        if img is None:
            continue
        
        for track_id, x, y, w, h in detections[frame_id]:
            track_folder = os.path.join(output_folder, f"player_{track_id:03d}")
            os.makedirs(track_folder, exist_ok=True)
            
            x1 = max(0, x)
            y1 = max(0, y)
            x2 = min(img.shape[1], x + w)
            y2 = min(img.shape[0], y + h)
            
            if x2 <= x1 or y2 <= y1:
                continue
            
            crop = img[y1:y2, x1:x2]

            # Cambiado el nombre del archivo al formato deseado: frameId_trackId.jpg
            output_filename = f"{frame_id:06d}_{track_id:03d}.jpg"
            output_path = os.path.join(track_folder, output_filename)
            cv2.imwrite(output_path, crop)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mot_file', required=True)
    parser.add_argument('--image_folder', required=True)
    parser.add_argument('--output_folder', required=True)
    
    args = parser.parse_args()
    
    print("Leyendo archivo MOT...")
    detections = parse_mot_file(args.mot_file)
    
    print("\nRecortando detecciones...")
    crop_and_save_detections(args.image_folder, detections, args.output_folder)
    
    print(f"\nProceso completado. Recortes en: {args.output_folder}")

if __name__ == "__main__":
    main()


#python dicMaker_idPlayer.py --mot_file "C:\Users\jismbs\Documents\gta-link\DeepEIoU_trackerVideo2_Split+Connect_eps0.6_minSamples10_K3_mergeDist0.4_spatial1.0\video2.txt" --image_folder "C:\Users\jismbs\Documents\gta-link\frames_trackerVideo2\video2\img1" --output_folder "C:\Users\jismbs\Documents\gta-link\player_crops2"