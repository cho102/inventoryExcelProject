import re
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://192.168.1.12/som/")

    #Login
    print(page.title())
    input("Website loaded. Log in using the browser window and press Enter to continue. ..")
    print("Logged in. Browser stays open.")

    #Search for SKU
    sku = "FC20600"
    page.locator("#ContentPlaceHolder1_TextBoxSKU").fill(sku)
    page.locator("#ContentPlaceHolder1_ButtonSubmit").click()
    page.wait_for_load_state("domcontentloaded")
    print("Search completed. Check the browser window for results.")

    #Find inventory of SKU
    row = page.locator("tr").filter(has_text=sku).first
    cells = row.locator("td")
    print("Number of cells in the row:", cells.count())
    details = cells.nth(13).inner_text()

    print("\nRaw inventory details for SKU", sku, ":\n", details)

    #created list of inventory by color
    lines = details.strip().splitlines()
    pattern = rf"{sku}\s+(.*?)\s+\((\d+)\)"
    
    print("\nSeparated details:")
    for line in lines:
        match = re.search(pattern, line)

    if match:
        color = match.group(1).strip()
        quantity = int(match.group(2))

        print("Color:", color)
        print("Quantity:", quantity)

    #Task done
    input("Press Enter to close the browser and exit the script. ..")
    browser.close()
