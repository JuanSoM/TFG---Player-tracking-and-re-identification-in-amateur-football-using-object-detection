import os
import torch
from datasets.sportsreid_dataset import register_dataset
from models.model_builder import build_model
from engine.trainer import get_datamanager, train_model

def main():
    # Registrar dataset personalizado
    register_dataset()
    
    # Configuración
    dataset_dir = r'C:\Users\Soriano\OneDrive\Documentos\entrenamientoReID\player_crops2_reid'
    save_dir = 'log/osnet_sportsreid'
    from datasets.sportsreid_dataset import SportsReIDDataset
    # Después de registrar el dataset
    test = SportsReIDDataset(
        root=r'C:\Users\Soriano\OneDrive\Documentos\entrenamientoReID\player_crops2_reid',
        mode='train'
    )
    print("\nPrimer elemento de train:", test.train[0])
    print("Primer elemento de query:", test.query[0] if test.query else "N/A")
    print("Primer elemento de gallery:", test.gallery[0] if test.gallery else "N/A")
    # Verificación directa
    test_dataset = SportsReIDDataset(
        root=r'C:\Users\Soriano\OneDrive\Documentos\entrenamientoReID\player_crops2_reid',
        mode='train'
    )
    print(f"Dataset cargado correctamente con {len(test_dataset.train)} train, {len(test_dataset.query)} query, {len(test_dataset.gallery)} gallery samples")
    
    # Inicializar
    datamanager = get_datamanager(dataset_dir)

    num_classes = datamanager.num_train_pids
    model = build_model(num_classes)
    
    # Entrenar
    engine = train_model(datamanager, model, save_dir)
    
    # Guardar modelo
    torch.save(model.state_dict(), 'osnet_sportsreid.pth')
    print("Modelo guardado como 'osnet_sportsreid.pth'")
    
    # Evaluación final
    #print("\nEvaluación final:")
    #engine.test()

if __name__ == '__main__':
    main()