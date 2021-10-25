
def crypto_image_path(instance, filename):
    extension = filename.split(".")[-1]
    return f'crypto/{instance.symbol}.{extension}'
