import re
from playwright.sync_api import sync_playwright

def get_inventory(page, sku):
    #Login
    # print(page.title())
    # input("Website loaded. Log in using the browser window and press Enter to continue. ..")
    # print("Logged in. Browser stays open.")

    #Search for SKU
    page.locator("#ContentPlaceHolder1_TextBoxSKU").fill(sku)
    page.locator("#ContentPlaceHolder1_ButtonSubmit").click()
    page.wait_for_load_state("domcontentloaded")
    print("Search completed for SKU:", sku)

    #Find inventory of SKU
    row = page.locator("tr").filter(has_text=sku).first
    cells = row.locator("td")
    # get the Details column (14th column, index 13)
    details = cells.nth(13).inner_text()
    # print("\nRaw inventory details for SKU", sku, ":\n", details)

    #created list of inventory by color
    inventory = []

    lines = details.strip().splitlines()
    pattern = rf"{sku}\s+(.*?)\s+\((\d+)\)"
        
    # print("\nSeparated details:")
    for line in lines:
        match = re.search(pattern, line)

        if match:
            color = match.group(1).strip()
            quantity = int(match.group(2))
            # print("Color:", color)
            # print("Quantity:", quantity)
            inventory.append((color, quantity))

    return inventory