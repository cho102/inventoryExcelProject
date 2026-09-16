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