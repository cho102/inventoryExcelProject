from text_processing import read_product_list, find_product_photo, get_all_product_skus

# skus_list = read_product_list("product_list.txt")
PHOTO_FOLDER = "photos"
PRODUCT_LIST_FILE = "product_list.txt"

with open(PRODUCT_LIST_FILE, 'r') as f:
   product_list = f.read()

skus = get_all_product_skus(product_list, PHOTO_FOLDER)

for sku in skus:
    print(f"SKU: {sku}")

print(f"Total SKUs found: {len(skus)}")