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
