LEFT = {
      "picture_col": 1, 
      "product_col": 5, 
      "color_col": 6, 
      "qty_col": 7, 
      "price_col": 8
      }

RIGHT = {
      "picture_col": 10, 
      "product_col": 14, 
      "color_col": 15, 
      "qty_col": 16, 
      "price_col": 17
      }

def setup_sheet(sheet):

    # Headers
    headers = {
        "A1": "Product Picture",
        "E1": "Product Name",
        "F1": "Colors",
        "G1": "Qty",
        "H1": "Price",

        "J1": "Product Picture",
        "N1": "Product Name",
        "O1": "Colors",
        "P1": "Qty",
        "Q1": "Price",
    }

    for cell, value in headers.items():
        sheet[cell] = value

    # Picture columns
    for column in ["A", "B", "C", "D", "J", "K", "L", "M"]:
        sheet.column_dimensions[column].width = 12

    # Information columns
    for column in ["E", "N"]:
        sheet.column_dimensions[column].width = 15

    for column in ["F", "G", "H", "O", "P", "Q"]:
        sheet.column_dimensions[column].width = 10

def add_inventory(sheet, curr_row, columns, sku, cost, inventory):
   