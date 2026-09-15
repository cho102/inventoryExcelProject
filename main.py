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

#create a new Excel workbook
workbook = Workbook()

#select the active worksheet
sheet = workbook.active

#create column headers
sheet['A1'] = "Product Picture"
sheet['E1'] = "Product Name"
sheet['F1'] = "Colors"
sheet['G1'] = "Qty"
sheet['H1'] = "Price"
sheet['J1'] = "Product Picture"
sheet['N1'] = "Product Name"
sheet['O1'] = "Colors"
sheet['P1'] = "Qty"
sheet['Q1'] = "Price"

#create column widths:
sheet.column_dimensions["A"].width = 12
sheet.column_dimensions["B"].width = 12
sheet.column_dimensions["C"].width = 12
sheet.column_dimensions["D"].width = 12
sheet.column_dimensions["J"].width = 12
sheet.column_dimensions["K"].width = 12
sheet.column_dimensions["L"].width = 12
sheet.column_dimensions["M"].width = 12

sheet.column_dimensions["E"].width = 15
sheet.column_dimensions["F"].width = 10
sheet.column_dimensions["G"].width = 10
sheet.column_dimensions["H"].width = 10
sheet.column_dimensions["N"].width = 15
sheet.column_dimensions["O"].width = 10
sheet.column_dimensions["P"].width = 10
sheet.column_dimensions["Q"].width = 10

left_start_col = 1    # A
right_start_col = 10  # J

#START BROWSER
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="login_state.json")
    page = context.new_page()
     
    page.goto("http://192.168.1.12/som/query_sm.aspx")

    #read image files and add to excel
    files = os.listdir(photo_folder)
    curr_row = 2

    left = True
    left_rows_used = 0

    for file in image_files:
        #format data
        if left:
          picture_col = 1
          product_col = 5
          color_col = 6
          qty_col = 7
          price_col = 8
        else:
          picture_col = 10
          product_col = 14
          color_col = 15
          qty_col = 16
          price_col = 17
      
        sku = file.split(".")[0]
        # print(f"Adding product: {sku} at row {curr_row}")

        #GET COST & INVENTORY
        cost, inventory = get_inventory(page, sku)
        # print(f"\nFinal inventory list for SKU {sku}:", inventory)

        inventory_row = curr_row
        #add inventory details to excel
        for color, quantity in inventory:
            sheet.cell(row=inventory_row, column=product_col, value=sku)
            sheet.cell(row=inventory_row, column=color_col, value=color)
            sheet.cell(row=inventory_row, column=qty_col, value=quantity)
            sheet.cell(row=inventory_row, column=price_col, value=cost)
            inventory_row += 1

        # Create the image
        image_path = os.path.join(photo_folder, file)
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
        sheet.add_image(image, f"{chr(64 + picture_col)}{curr_row}")

    
        rows_used = max(len(inventory) + 1, photo_rows)
        
        if left:
            # Remember how many rows the left product used
            left_rows_used = rows_used
            left = False
        else:
            # Move down based on whichever product was taller
            # curr_row = rows_used + curr_row + 2
            curr_row += max(left_rows_used, rows_used) + 2
            left = True

        print("rows used:", rows_used)
        print("current row:", curr_row)

    #save excel
    date = datetime.now().strftime("%Y%m%d")
    name = "inStockInventory"
    workbook.save(f"{name}_{date}.xlsx")
    browser.close()

#check
print("Excel file created successfully!")
