import os

def get_photo_files(photo_folder):
    files = os.listdir(photo_folder)

    image_files = sorted([
        file for file in files
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ])

    return image_files


def get_photo_sku(filename):
    return filename.split(".")[0]
