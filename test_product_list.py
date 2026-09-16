from text_processing import read_product_list, find_product_photo

skus_list = read_product_list("product_list.txt")
PHOTO_FOLDER = "photos"

for sku in skus_list:
    photo = find_product_photo(sku, PHOTO_FOLDER)
    if photo:
        print(f"{sku} -> {photo}")
    else:
        print(f"{sku} -> No photo found")
print(skus_list)