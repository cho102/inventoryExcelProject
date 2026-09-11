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
sheet['A2'] = "Product Name"
sheet['A3'] = "Colors"
sheet['A4'] = "Qty"
sheet['A5'] = "Price"

row = 2

for file in image_files:
    product_name = file.split(".")[0]

    # Create the image
    image_path = os.path.join(photo_folder, file)
    image = Image(image_path)

    # Resize the image
    image.width = 150
    image.height = 150

    # Put the image into column A
    worksheet.add_image(image, f"A{row}")

    # Put the product name into column B
    sheet.cell(row=row, column=2, value=product_name)

row += 1

#save excel
workbook.save("inStockInventory.xlsx")

#check
print("Excel file created successfully!")
