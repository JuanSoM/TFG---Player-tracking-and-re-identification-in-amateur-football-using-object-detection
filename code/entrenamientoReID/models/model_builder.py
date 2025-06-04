from torchreid import models

def build_model(num_classes):
    model = models.build_model(
        name='osnet_x1_0',
        num_classes=num_classes,
        loss='softmax',
        pretrained=True,
        use_gpu=True
    )
    return model