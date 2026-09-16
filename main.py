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
# from text_processing import get_product_skus

#access photos folder
photo_folder = "photos"
image_files = get_photo_files(photo_folder)
# files = os.listdir(photo_folder)

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
# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context(storage_state="login_state.json")
#     page = context.new_page()
     
#     page.goto("http://192.168.1.12/som/query_sm.aspx")

curr_row = 2

left = True
left_rows_used = 0

successful = 0
no_inventory = 0
errors = 0

#Handle duplciate skus
processed_skus = set()


for file in image_files:
    columns = LEFT if left else RIGHT
    
    sku = get_photo_sku(file)

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
    # image_path = os.path.join(photo_folder, file)
    # image = Image(image_path)

    # # Resize the image
    # new_width = 288
    # new_height = int(image.height * (new_width / image.width))
    # image.width = new_width
    # image.height = new_height

    # # Calculate the number of rows the image will occupy
    # row_height = 15  # Adjust this value based on your row height
    # photo_rows = int((image.height * 0.75) / row_height) + 1  # 0.75 is a scaling factor for Excel row height

    # # Put the image into column A/J
    # sheet.add_image(image, f"{chr(64 + picture_col)}{curr_row}")
    picture_col = "A" if left else "J"
    photo_rows = add_photo(sheet, curr_row, picture_col, photo_folder, file)


    rows_used = max(len(inventory) + 1, photo_rows)
    
    # if left:
    #     # Remember how many rows the left product used
    #     left_rows_used = rows_used
    #     left = False
    # else:
    #     # Move down based on whichever product was taller
    #     curr_row += max(left_rows_used, rows_used) + 2
    #     left = True
    curr_row, left_rows_used, left = update_position(curr_row, left_rows_used, rows_used, left)

    print("rows used:", rows_used)
    print("current row:", curr_row)

print("\n--- Summary ---")
print(f"Successful: {successful}")
print(f"No inventory: {no_inventory}")
print(f"Errors: {errors}")
print(f"Total products: {len(image_files)}")


#save excel
date = datetime.now().strftime("%Y%m%d")
name = "inStockInventory"
workbook.save(os.path.join(output_folder, f"{name}_{date}.xlsx"))
browser.close()

#check
print("Excel file created successfully!")
