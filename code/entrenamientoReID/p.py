import os

def get_ids_from_split(split_dir):
    return set(os.listdir(split_dir))

# Paths a tus carpetas
base_dir = r"C:\Users\Soriano\OneDrive\Documentos\entrenamientoReID\player_crops2_reid"
query_ids = get_ids_from_split(os.path.join(base_dir, 'query'))
gallery_ids = get_ids_from_split(os.path.join(base_dir, 'gallery'))

missing_ids = query_ids - gallery_ids

print("IDs en query que NO están en gallery:", missing_ids)
print(f"Total IDs en query: {len(query_ids)}, en gallery: {len(gallery_ids)}")
