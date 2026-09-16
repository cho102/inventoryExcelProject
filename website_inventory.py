import re
from playwright.sync_api import sync_playwright

def start_browser():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="login_state.json")
    page = context.new_page()
    page.goto("http://192.168.1.12/som/query_sm.aspx")
    return playwright, browser, context, page

def get_inventory(page, sku):
    #Search for SKU
    page.locator("#ContentPlaceHolder1_TextBoxSKU").fill(sku)
    page.locator("#ContentPlaceHolder1_ButtonSubmit").click()
    page.wait_for_load_state("domcontentloaded")

    #Find inventory of SKU
    row = page.locator("tr").filter(has_text=sku).first
    try:
        row.wait_for(timeout=10000)
    except:
        raise Exception(f"SKU {sku} not found or search timed out")

    
    cells = row.locator("td")
    
    #get cost column
    cost_text = cells.nth(11).inner_text().strip()
    try:
        cost = float(cost_text)
    except ValueError:
        raise Exception(f"Invalid cost for SKU {sku}: {cost_text}")

    # get the Details column (14th column, index 13)
    details = cells.nth(13).inner_text()
    if not details:
        return cost, []
    print("DETAILS:")
    print(details)
    #created list of inventory by color
    inventory = []

    lines = details.strip().splitlines()
    pattern = rf"{re.escape(sku)}(?:\s+SET)?\s+(.*?)\s+\((\d+)\)"
        
    for line in lines:
        match = re.search(pattern, line)

        if match:
            color = match.group(1).strip()
            quantity = int(match.group(2))
            inventory.append((color, quantity))

    return cost, inventory
