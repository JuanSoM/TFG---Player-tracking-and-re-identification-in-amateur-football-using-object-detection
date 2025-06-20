import os
import shutil
import random
from pathlib import Path

# Parámetros
source_dir = Path(r"C:\Users\jismbs\Documents\gta-link\player_crops2")
target_dir = Path(r"C:\Users\jismbs\Documents\gta-link\player_crops2_reid")

train_ratio = 0.7
query_ratio = 0.15
gallery_ratio = 0.15

# Asegúrate de que suman 1.0
assert abs(train_ratio + query_ratio + gallery_ratio - 1.0) < 1e-6

splits = ['train', 'query', 'gallery']

for split in splits:
    (target_dir / split).mkdir(parents=True, exist_ok=True)

# Para cada jugador (identidad)
for player_folder in source_dir.iterdir():
    if not player_folder.is_dir():
        continue
    
    images = list(player_folder.glob("*.jpg"))
    if len(images) < 3:
        print(f"Saltando {player_folder.name}: no hay suficientes imágenes (mínimo 3)")
        continue
    
    random.shuffle(images)
    n = len(images)
    n_train = int(n * train_ratio)
    n_query = int(n * query_ratio)

    split_counts = {
        'train': images[:n_train],
        'query': images[n_train:n_train + n_query],
        'gallery': images[n_train + n_query:]
    }

    for split, split_images in split_counts.items():
        split_target_dir = target_dir / split / player_folder.name
        split_target_dir.mkdir(parents=True, exist_ok=True)
        for img_path in split_images:
            shutil.copy(img_path, split_target_dir / img_path.name)

print("✅ Dataset reorganizado correctamente en formato Torchreid.")
