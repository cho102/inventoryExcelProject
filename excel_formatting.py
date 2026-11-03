LEFT = {
      "picture_col": 1, 
      "product_col": 5, 
      "color_col": 6, 
      "qty_col": 7, 
      "price_col": 8,
      "cost_col": 9
      }

RIGHT = {
      "picture_col": 11, 
      "product_col": 15, 
      "color_col": 16, 
      "qty_col": 17, 
      "price_col": 18
      "cost_col": 19
      }

NO_PHOTO_ROWS = 15

def setup_sheet(sheet):

    # Headers
    headers = {
        "A1": "Product Picture",
        "E1": "Product Name",
        "F1": "Colors",
        "G1": "Qty",
        "H1": "Price",
        "I1": "Cost",

        "K1": "Product Picture",
        "O1": "Product Name",
        "P1": "Colors",
        "Q1": "Qty",
        "R1": "Price",
        "S1": "Cost"
    }

    for cell, value in headers.items():
        sheet[cell] = value

    # Picture columns
    for column in ["A", "B", "C", "D", "N","K", "L", "M"]:
        sheet.column_dimensions[column].width = 12

    # Information columns
    for column in ["E", "O"]:
        sheet.column_dimensions[column].width = 15

    for column in ["F", "G", "H", "I", "R", "P", "Q", "S"]:
        sheet.column_dimensions[column].width = 10

def add_inventory(sheet, curr_row, columns, sku, cost, price, inventory):
    if not inventory:  # No inventory found
        sheet.cell(row=curr_row, column=columns["product_col"], value=sku)
        sheet.cell(row=curr_row, column=columns["color_col"], value="No inventory")
        return 1

    for row, (color, quantity) in enumerate(inventory, start=curr_row):
        sheet.cell(row=row, column=columns["product_col"], value=sku)
        sheet.cell(row=row, column=columns["color_col"], value=color)
        sheet.cell(row=row, column=columns["qty_col"], value=quantity)
        sheet.cell(row=row, column=columns["price_col"], value=price)
        sheet.cell(row=row, column=columns["cost_col"], value=cost)

    return len(inventory)

def add_error(sheet, curr_row, columns, sku, error_message):
    sheet.cell(row=curr_row, column=columns["product_col"], value=sku)
    sheet.cell(row=curr_row, column=columns["color_col"], value="ERROR")
    sheet.cell(row=curr_row, column=columns["qty_col"], value=error_message)
    return 1

def add_no_inventory(sheet, curr_row, columns, sku):
    sheet.cell(row=curr_row, column=columns["product_col"], value=sku)
    sheet.cell(row=curr_row, column=columns["color_col"], value="No inventory")
    return 1

def update_position(curr_row, left_rows_used, rows_used, left):
    if left:
        # Remember how many rows the left product used
        left_rows_used = rows_used
        left = False
    else:
        # Move down based on whichever product was taller
        curr_row += max(left_rows_used, rows_used) + 2
        left = True
        
    return curr_row, left_rows_used, left