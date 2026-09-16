from playwright.sync_api import sync_playwright
from text_processing import read_product_list
from website_inventory import get_inventory

PRODUCT_LIST = "product_list.txt"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(
        storage_state = "login_state.json"
    )
    page = context.new_page()

    page.goto("http://192.168.1.12/som/query_sm.aspx")

    skus_list = read_product_list(PRODUCT_LIST)

    for sku in skus_list:
        print(f"Checking inventory for SKU: {sku}")
        try:
            cost, inventory = get_inventory(page, sku)
            print(f"SKU: {sku}\nCost: {cost}\nInventory: {inventory}\n")
        except Exception as e:
            print(f"Error occurred while checking inventory for SKU {sku}: {e}")

    browser.close()