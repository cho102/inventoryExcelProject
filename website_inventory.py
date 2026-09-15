import re
from playwright.sync_api import sync_playwright

def get_inventory(sku):
        

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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="login_state.json")
    page = context.new_page()
     
    page.goto("http://192.168.1.12/som/query_sm.aspx")

    #test the function
    skus = ["FC20600", "FC19784"]
    for sku in skus:
        inventory = get_inventory(sku)
        print(f"\nFinal inventory list for SKU {sku}:", inventory)

    #Task done
    # input("Press Enter to close the browser and exit the script. ..")
    browser.close()