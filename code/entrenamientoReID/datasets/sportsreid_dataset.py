import os
from torchreid.reid.data import ImageDataset
from torchreid.reid.data import register_image_dataset

class SportsReIDDataset(ImageDataset):
    def __init__(self, root, **kwargs):
        self.root = root

        # Primero recolectamos todos los pid únicos
        pid_set = set()
        for subset in ['train', 'query', 'gallery']:
            subset_dir = os.path.join(self.root, subset)
            if not os.path.exists(subset_dir):
                continue
            for player_dir in os.listdir(subset_dir):
                if player_dir.startswith('player_'):
                    try:
                        pid = int(player_dir.split('_')[-1])
                        pid_set.add(pid)
                    except ValueError:
                        continue

        # Creamos el mapeo de pid original a pid reindexado
        self.pid2label = {pid: idx for idx, pid in enumerate(sorted(pid_set))}

        # Cargamos los datasets aplicando el mapeo
        train_data = self._load_set('train')
        query_data = self._load_set('query')
        gallery_data = self._load_set('gallery')

        # Asegura compatibilidad con Torchreid
        if not train_data:
            train_data = [('dummy_train.jpg', 0, 0, 0)]
        if not query_data:
            query_data = [('dummy_query.jpg', 0, 0, 0)]
        if not gallery_data:
            gallery_data = [('dummy_gallery.jpg', 0, 0, 0)]

        super().__init__(
            train=train_data,
            query=query_data,
            gallery=gallery_data,
            **kwargs
        )

    def _load_set(self, subset):
        data = []
        subset_dir = os.path.join(self.root, subset)

        if not os.path.exists(subset_dir):
            return data

        if subset == 'query':
            camid = 0
        elif subset == 'gallery':
            camid = 1
        else:  # train
            camid = 2

        for player_dir in sorted(os.listdir(subset_dir)):
            if not player_dir.startswith('player_'):
                continue
                
            try:
                pid_original = int(player_dir.split('_')[-1])
                pid = self.pid2label[pid_original]
            except ValueError:
                continue

            player_path = os.path.join(subset_dir, player_dir)
            for img_name in sorted(os.listdir(player_path)):
                if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(player_path, img_name)
                    data.append((img_path, pid, camid, 0))  # dsetid=0
        return data


def register_dataset():
    register_image_dataset('sportsreid', SportsReIDDataset)
