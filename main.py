import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image 
from playwright.sync_api import sync_playwright
from datetime import datetime

from website_inventory import get_inventory

#access photos folder
photo_folder = "photos"
files = os.listdir(photo_folder)

#check for images only
image_files = [file for file in files 
               if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

#find product names from image files
#product_names = [file.split(".")[0] for file in image_files]

#check
# print("Image files in the folder:")
# for file in image_files:
#     print(file)
#     # print("Product name:", file.split(".")[0])
# print("Image files in the folder:")
# for product in product_names:
#     print(product)

#create a new Excel workbook
workbook = Workbook()

#select the active worksheet
sheet = workbook.active

#name the worksheet
sheet.title = "inStockInventory"

#create column headers
sheet['A1'] = "Product Picture"
sheet['E1'] = "Product Name"
sheet['F1'] = "Colors"
sheet['G1'] = "Qty"
sheet['H1'] = "Price"

#create column widths:
sheet.column_dimensions["A"].width = 12
sheet.column_dimensions["B"].width = 12
sheet.column_dimensions["C"].width = 12
sheet.column_dimensions["D"].width = 12

sheet.column_dimensions["E"].width = 15
sheet.column_dimensions["F"].width = 10
sheet.column_dimensions["G"].width = 10
sheet.column_dimensions["H"].width = 10


#START BROWSER
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="login_state.json")
    page = context.new_page()
     
    page.goto("http://192.168.1.12/som/query_sm.aspx")



    #read image files and add to excel
    files = os.listdir(photo_folder)
    curr_row = 2

    for file in image_files:
        image_files = [file for file in files 
                        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        sku = file.split(".")[0]
        # print(f"Adding product: {sku} at row {curr_row}")


        #GET INVENTORY
        inventory = get_inventory(page, sku)
        # print(f"\nFinal inventory list for SKU {sku}:", inventory)

        inventory_row = curr_row
        #add inventory details to excel
        for color, quantity in inventory:
            sheet.cell(row=inventory_row, column=5, value=sku)
            sheet.cell(row=inventory_row, column=6, value=color)
            sheet.cell(row=inventory_row, column=7, value=quantity)
            inventory_row += 1

        
        # Create the image
        image_path = os.path.join(photo_folder, file)
        image = Image(image_path)

        # Resize the image
        new_width = 325
        # new_height = 250
        new_height = int(image.height * (new_width / image.width))
        image.width = new_width
        image.height = new_height

        # Calculate the number of rows the image will occupy
        row_height = 35  # Adjust this value based on your row height
        photo_rows = int((image.height * 0.75) / row_height) + 1  # 0.75 is a scaling factor for Excel row height
        # Put the image into column A
        sheet.add_image(image, f"A{curr_row}")

    
        rows_used = max(len(inventory) + 1, photo_rows)
        curr_row = rows_used + curr_row + 15

        print("rows used:", rows_used)
        print("current row:", curr_row)
        

    #save excel
    date = datetime.now().strftime("%Y%m%d")
    workbook.save(f"inStockInventory_{date}.xlsx")
    browser.close()

#check
print("Excel file created successfully!")
