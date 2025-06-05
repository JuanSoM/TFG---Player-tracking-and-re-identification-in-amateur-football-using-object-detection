import torchreid
from datasets.sportsreid_dataset import register_dataset

def main():
    # Registra el dataset
    register_dataset()

    # Carga datos
    datamanager = torchreid.data.ImageDataManager(
        root='C:/Users/Soriano/OneDrive/Documentos/entrenamientoReID/player_crops2_reid',
        sources='sportsreid',
        height=256,
        width=128,
        batch_size_train=32,
        batch_size_test=100,
        transforms=['random_flip'],
        use_gpu=True
    )

    # Carga modelo y pesos
    model = torchreid.models.build_model(
        name='resnet50_fc512',
        num_classes=datamanager.num_train_pids,
        loss='softmax',
        pretrained=False
    )

    torchreid.utils.load_pretrained_weights(
        model,
        r'C:\Users\Soriano\OneDrive\Documentos\entrenamientoReID\reid_checkpoints\model.resnet50.pth.tar-20'
    )

    # Crear el motor y lanzar evaluación
    engine = torchreid.engine.ImageSoftmaxEngine(
        datamanager,
        model,
        optimizer=None  # Solo evaluamos, no entrenamos
    )

    engine.test()

if __name__ == '__main__':
    main()
