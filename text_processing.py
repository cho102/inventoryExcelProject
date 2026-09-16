import os

def find_product_photo(sku, photo_folder):
    # Get the list of photo files in the folder
    photo_files = os.listdir(photo_folder)
    
    # Iterate through the photo files to find a match for the SKU
    for photo_file in photo_files:
        photo_sku = photo_file.split('.')[0]  # Assuming the SKU is the filename without extension
        # print(f"Checking photo file: {photo_file}, extracted SKU: {photo_sku.split(' ')[0]}")
        if photo_sku.upper() == sku.upper() or photo_sku.split(' ')[0].upper() == sku.upper():
            return photo_file  # Return the matching photo file name

    return None  # Return None if no matching photo is found

def get_product_skus(product_list):
    skus = []
    processed_skus = set()  # To track duplicates
    lines = product_list.splitlines()  # Split the text into lines

    for name in lines:
        sku = name.strip()

        if not sku:
            continue

        if sku in processed_skus:
            continue

        processed_skus.add(sku)   
        skus.append(sku)
        
    return skus

def read_product_list(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    return get_product_skus(text)