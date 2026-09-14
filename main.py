import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image

#access photos folder
photo_folder = "photos"

#images 
files = os.listdir(photo_folder)
#check for images only
image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

#find product names from image files
product_names = [file.split(".")[0] for file in image_files]

#check
print("Image files in the folder:")
for file in image_files:
    print(file)
    # print("Product name:", file.split(".")[0])
print("Image files in the folder:")
for product in product_names:
    print(product)

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



curr_row = 2

for file in image_files:
    product_name = file.split(".")[0]

    start_row = curr_row
    print(f"Adding product: {product_name} at row {start_row}")
    # Create the image
    image_path = os.path.join(photo_folder, file)
    image = Image(image_path)

    # Resize the image
    new_width = 325
    new_height = int(image.height * (new_width / image.width))
    image.width = new_width
    image.height = new_height

    # Put the image into column A
    sheet.add_image(image, f"A{start_row}")

    # Put the product name into column E
    sheet.cell(row=start_row, column=5, value=product_name)

    curr_row += 17

#save excel
workbook.save("inStockInventory.xlsx")

#check
print("Excel file created successfully!")
