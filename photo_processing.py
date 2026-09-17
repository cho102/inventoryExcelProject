import os
import re
from openpyxl.drawing.image import Image

def get_photo_files(photo_folder):
    files = os.listdir(photo_folder)

    image_files = sorted([
        file for file in files
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
    ])

    return image_files


def get_photo_sku(filename):
    name = filename.upper()
    
    # Convert underscores back to spaces
    name = name.replace("_", " ")
    
    #get everything before .SERIES if it exists
    name = re.split(r"\.SERIES", name, maxsplit = 1)[0]

    #remove file extension
    name = re.sub(r"\.[^.]+$","", name)

    #remove trailing number
    name = re.sub(r"\s+\d+$","",name)

    return name.strip()

def add_photo(sheet, row, column, photo_folder, filename):
    image_path = os.path.join(photo_folder, filename)
    image = Image(image_path)

    # Resize the image
    new_width = 288
    new_height = int(image.height * (new_width / image.width))
    image.width = new_width
    image.height = new_height
    
    # Calculate the number of rows the image will occupy
    row_height = 15  # Adjust this value based on your row height
    photo_rows = int((image.height * 0.75) / row_height) + 1  # 0.75 is a scaling factor for Excel row height

    # Put the image into column A/J
    sheet.add_image(image, f"{column}{row}")
    
    return photo_rows
