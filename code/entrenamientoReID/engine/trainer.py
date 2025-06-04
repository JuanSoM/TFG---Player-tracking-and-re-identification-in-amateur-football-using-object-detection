from torchreid import optim, engine 
from torchreid.reid.data import ImageDataManager

def get_datamanager(dataset_dir):
    datamanager = ImageDataManager(
        root=dataset_dir,
        sources='sportsreid',
        targets='sportsreid',
        height=256,
        width=128,
        batch_size_train=32,
        batch_size_test=100,
        transforms=['random_flip', 'color_jitter'],
        norm_mean=[0.485, 0.456, 0.406],
        norm_std=[0.229, 0.224, 0.225],
        use_gpu=True
    )
    return datamanager

def train_model(datamanager, model, save_dir='log/osnet_sportsreid'):
    optimizer = optim.build_optimizer(
        model,
        optim='adam',
        lr=0.0003
    )
    
    scheduler = optim.build_lr_scheduler(
        optimizer,
        lr_scheduler='single_step',
        stepsize=20
    )
    
    reid_engine = engine.ImageSoftmaxEngine(
        datamanager,
        model,
        optimizer=optimizer,
        scheduler=scheduler,
        label_smooth=True,
        use_gpu=True
    )
    
    reid_engine.run(
        save_dir=save_dir,
        max_epoch=1,#10
        eval_freq=-1,#10
        print_freq=10,
        test_only=False,
        visrank=False
    )
    
    return reid_engine
