import os
import os.path as osp
from torchreid.data import ImageDataset
import torchreid
import re

class SoccerNetReIDDataset(ImageDataset):
    dataset_dir = 'soccernetv3/reid'
    
    def __init__(self, root='', **kwargs):
        self.root = osp.abspath(osp.expanduser(root))
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        
        # Inicializamos listas para cada conjunto
        train, query, gallery = [], [], []
        
        # Procesamos cada conjunto con su estructura específica
        self.process_dataset('train', train)  # Train no tiene query/gallery
        self.process_query_gallery('valid', query, gallery)
        self.process_query_gallery('test', query, gallery)
        self.process_challenge('challenge', query, gallery)
        
        # Llamada al padre con los conjuntos organizados
        super(SoccerNetReIDDataset, self).__init__(train, query, gallery, **kwargs)
    
    def process_dataset(self, subset, data_list):
        """Procesa train (sin subcarpetas query/gallery)"""
        subset_path = osp.join(self.dataset_dir, subset)
        
        if not osp.exists(subset_path):
            print(f"Advertencia: Directorio {subset_path} no encontrado")
            return
        
        for root, _, files in os.walk(subset_path):
            for file in files:
                if file.endswith('.png'):
                    filepath = osp.join(root, file)
                    person_id, camera_id = self.parse_filename(file)
                    
                    if person_id is not None:
                        data_list.append((filepath, person_id, camera_id))
    
    def process_query_gallery(self, subset, query_list, gallery_list):
        """Procesa valid/test que tienen subcarpetas query/gallery"""
        for subset_type in ['query', 'gallery']:
            subset_path = osp.join(self.dataset_dir, subset, subset_type)
            
            if not osp.exists(subset_path):
                print(f"Advertencia: Directorio {subset_path} no encontrado")
                continue
                
            for root, _, files in os.walk(subset_path):
                for file in files:
                    if file.endswith('.png'):
                        filepath = osp.join(root, file)
                        person_id, camera_id = self.parse_filename(file)
                        
                        if person_id is not None:
                            if subset_type == 'query':
                                query_list.append((filepath, person_id, camera_id))
                            else:
                                gallery_list.append((filepath, person_id, camera_id))
    
    def process_challenge(self, subset, query_list, gallery_list):
        """Procesa challenge que tiene subcarpetas query/gallery con formato diferente"""
        for subset_type in ['query', 'gallery']:
            subset_path = osp.join(self.dataset_dir, subset, subset_type)
            
            if not osp.exists(subset_path):
                print(f"Advertencia: Directorio {subset_path} no encontrado")
                continue
                
            for root, _, files in os.walk(subset_path):
                for file in files:
                    if file.endswith('.png'):
                        filepath = osp.join(root, file)
                        # Challenge usa -1 como person_id (se ignorará en evaluación)
                        if subset_type == 'query':
                            query_list.append((filepath, -1, 0))
                        else:
                            gallery_list.append((filepath, -1, 0))
    
    def parse_filename(self, filename):
        """Extrae person_id y camera_id del nombre de archivo"""
        # Eliminamos la extensión y dividimos por '-'
        parts = filename[:-4].split('-')
        
        try:
            if len(parts) >= 8:  # Formato estándar
                person_uid = parts[2]
                action_idx = parts[1]
                
                # Creamos IDs consistentes
                person_id = self.get_numeric_id(person_uid)
                camera_id = self.get_numeric_id(action_idx) % 10  # Limitar a 10 cámaras
                
                return person_id, camera_id
            
            elif len(parts) == 3 and 'x' in parts[2]:  # Formato challenge
                return None, 0
            
        except Exception as e:
            print(f"Error procesando {filename}: {str(e)}")
            return None, 0
        
        return None, 0
    
    def get_numeric_id(self, uid):
        """Convierte cualquier UID a un número entero único"""
        if uid.isdigit():
            return int(uid)
        else:
            # Para IDs no numéricos (como 'a', 'f', etc.) usamos hash
            return abs(hash(uid)) % (10**8)

# Registramos el dataset
torchreid.data.register_image_dataset('soccernet_reid', SoccerNetReIDDataset)

if __name__ == '__main__':
    import torchreid
    from multiprocessing import freeze_support
    
    freeze_support()
    
    # Configuración mejorada del data manager
    datamanager = torchreid.data.ImageDataManager(
        root='C:/path/to/project/datasets',  # Ajusta esta ruta
        sources='soccernet_reid',
        targets='soccernet_reid',
        height=256,
        width=128,
        batch_size_train=64,
        batch_size_test=128,
        transforms=['random_flip', 'color_jitter', 'random_crop'],
        norm_mean=[0.485, 0.456, 0.406],
        norm_std=[0.229, 0.224, 0.225],
        use_gpu=True,
        split_id=0,
        combineall=False,
        num_instances=4,  # Para sampler por identidad
        train_sampler='RandomIdentitySampler'
    )
    
    # Construcción del modelo con más opciones
    model = torchreid.models.build_model(
        name="osnet_ain_x1_0",  # Versión mejorada de OSNet
        num_classes=datamanager.num_train_pids,
        loss="triplet",  # Combinación de triplet + softmax
        pretrained=True,
        use_gpu=True,
        last_stride=1
    )
    
    # Configuración avanzada del optimizador
    optimizer = torchreid.optim.build_optimizer(
        model,
        optim="adamw",
        lr=0.00035,
        weight_decay=5e-4,
        momentum=0.9,
        staged_lr=False,
        new_layers=None,
        base_lr_mult=0.1
    )
    
    # Scheduler con calentamiento
    scheduler = torchreid.optim.build_lr_scheduler(
        optimizer,
        lr_scheduler="cosine_annealing",
        warmup_epoch=5,
        max_epoch=120,
        eta_min_lr=1e-7
    )
    
    # Motor de entrenamiento mejorado
    engine = torchreid.engine.ImageTripletEngine(
        datamanager,
        model,
        optimizer=optimizer,
        scheduler=scheduler,
        margin=0.3,
        weight_t=1.0,
        weight_x=0.5,
        weight_htri=0.5,
        center_loss_weight=0.0005,
        use_center=True,
        use_htri=True,
        label_smooth=True,
        normalize_feature=True
    )
    
    # Entrenamiento con más opciones
    engine.run(
        save_dir="log/soccernet_reid_osnet_ain",
        max_epoch=120,
        eval_freq=5,
        print_freq=20,
        test_only=False,
        fixbase_epoch=10,
        open_layers=['classifier', 'layer4'],
        start_eval=20,
        visrank=False,
        save_model=True,
        pool_type='avg',
        dist_metric='euclidean',
        rerank=False
    )