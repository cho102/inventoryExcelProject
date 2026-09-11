import os
from openpyxl import Workbook

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
    print("Product name:", file.split(".")[0])

#create a new Excel workbook
workbook = Workbook()

#select the active worksheet
sheet = workbook.active

#name the worksheet
sheet.title = "Product Names"

#create column headers
sheet['A1'] = "Product Name"