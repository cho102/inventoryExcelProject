import os
import re
from io import BytesIO 
from PIL import Image as PILImage
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

def compress_image(image_path): 
    # Open original image 
    original = PILImage.open(image_path) 
    
    # Convert image to RGB 
    # This is needed when saving as JPEG. 
    if original.mode in ("RGBA", "LA", "P"): 
        background = PILImage.new("RGB", original.size, "white") 
        
        if original.mode == "P": 
            original = original.convert("RGBA") 
        
        background.paste( 
            original, 
            mask=original.getchannel("A") if original.mode == "RGBA" else None 
        ) 
        image = background 
    else: 
        image = original.convert("RGB") 
        
    # Limit the maximum dimensions. 
    # This reduces the amount of image data stored in Excel. 
    max_dimension = 1200 

    if image.width > max_dimension or image.height > max_dimension: 
        image.thumbnail( 
            (max_dimension, max_dimension), 
            PILImage.Resampling.LANCZOS 
        ) 
    
    # Save compressed JPEG into memory 
    compressed_image = BytesIO() 

    image.save( 
        compressed_image, 
        format="JPEG", 
        quality=75, 
        optimize=True 
    ) 
    compressed_image.seek(0)
    # Open the compressed image from memory 
    return PILImage.open(compressed_image)

def add_photo(sheet, row, column, photo_folder, filename):
    image_path = os.path.join(photo_folder, filename)
    # Compress the image before adding it to Excel
    compressed_image = compress_image(image_path)

    # Give the compressed image to openpyxl
    image = Image(compressed_image)

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
