def get_product_skus(product_list):
    skus = []

    for name in product_list:
        sku = name.strip()

        if sku:
            skus.append(sku)

    return skus