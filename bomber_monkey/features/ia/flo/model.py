import segmentation_models_pytorch as smp



model = smp.Unet(
    encoder_name="efficientnet-b7",
    encoder_weights="imagenet",
    in_channels=5,
    classes=1,
)