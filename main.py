import os
from openpyxl import Workbook
# from openpyxl.drawing.image import Image 
# from playwright.sync_api import sync_playwright
from datetime import datetime

from website_inventory import get_inventory, start_browser
from excel_formatting import (setup_sheet, add_inventory, 
                              add_error, add_no_inventory,
                              update_position, 
                              LEFT, RIGHT)
from photo_processing import add_photo, get_photo_files, get_photo_sku
from text_processing import get_all_product_skus, find_product_photo

FIXED_ROWS_NO_PHOTOS = 20

#access photos folder
photo_folder = "photos"
image_files = get_photo_files(photo_folder)
with open("product_list.txt", 'r') as f:
    product_list = f.read()

#access product list
product_list_file = "product_list.txt"
product_skus = get_all_product_skus(product_list, photo_folder)

#create output_folder
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

#create a new Excel workbook
workbook = Workbook()

#select the active worksheet
sheet = workbook.active
setup_sheet(sheet)

#START BROWSER
playwright, browser, context, page = start_browser()

curr_row = 2

left = True
left_rows_used = 0

successful = 0
no_inventory = 0
errors = 0

#Handle duplciate skus
processed_skus = set()


for sku in product_skus:
    columns = LEFT if left else RIGHT

    #check for duplicates
    if sku in processed_skus:
        print(f"Skipping duplicate SKU: {sku}")
        continue
    
    processed_skus.add(sku)

    #GET COST & INVENTORY
    try:
        cost, inventory = get_inventory(page, sku)
        error_message = None
    except Exception as e:
        #Can't find sku
        print(f"Error processing {sku}: {e}")
        cost = ""
        inventory = []
        error_message = str(e)
        errors += 1

    if error_message: #No SKU found
        inventory_rows = add_error(sheet, curr_row, columns, sku, error_message)
    elif not inventory: #No inventory found
        print(f"No inventory found for {sku}")
        inventory_rows = add_no_inventory(sheet, curr_row, columns, sku)
        no_inventory += 1
    else:
        inventory_rows = add_inventory(sheet, curr_row, columns, sku, cost, inventory)
        successful += 1

    # Create the image
    photo_file = None

    for file in image_files:
        if get_photo_sku(file).upper() == sku.upper():
            photo_file = file
            break

    #create image if it exists
    picture_col = "A" if left else "J"
    if photo_file:
        print(f"Adding photo for SKU: {sku}, file: {photo_file}")
        photo_rows = add_photo(sheet, curr_row, picture_col, photo_folder, photo_file)
    else:
        print(f"No photo found for SKU: {sku}")
        photo_rows = FIXED_ROWS_NO_PHOTOS  # Use a fixed number of rows for products without photos
    # photo_rows = add_photo(sheet, curr_row, picture_col, photo_folder, file)


    rows_used = max(len(inventory) + 1, photo_rows)
    
    curr_row, left_rows_used, left = update_position(curr_row, left_rows_used, rows_used, left)

    print("rows used:", rows_used)
    print("current row:", curr_row)

print("\n--- Summary ---")
print(f"Successful: {successful}")
print(f"No inventory: {no_inventory}")
print(f"Errors: {errors}")
print(f"Total products: {len(product_skus)}")


#save excel
date = datetime.now().strftime("%Y%m%d")
time = datetime.now().strftime("%H%M")
name = "inStockInventory"
workbook.save(os.path.join(output_folder, f"{name}_{date}{time}.xlsx"))
browser.close()

#check
print("Excel file created successfully!")
