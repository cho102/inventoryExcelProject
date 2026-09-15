from playwright.sync_api import sync_playwright
from website_inventory import get_inventory

# with sync_playwright() as p:

#     browser = p.chromium.launch(headless=False)

#     context = browser.new_context()

#     page = context.new_page()

#     # Open the inventory website
#     page.goto("http://192.168.1.12/som/query_sm.aspx")

#     # Log in manually
#     print("Please log in to the inventory website.")
#     input("After you finish logging in, press Enter here...")

#     # Save the login session
#     context.storage_state(path="login_state.json")

#     print("Login session saved!")

#     browser.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state="login_state.json")
    page = context.new_page()
     
    page.goto("http://192.168.1.12/som/query_sm.aspx")

    #test the function
    # skus = ["FC20600", "FC19784"]
    # for sku in skus:
    #     inventory = get_inventory(sku)
    #     print(f"\nFinal inventory list for SKU {sku}:", inventory)

    sku = "FC20600"  # Replace with the SKU you want to check
    inventory = get_inventory(page, sku)
    print(f"\nFinal inventory list for SKU {sku}:", inventory)

    #Task done
    # input("Press Enter to close the browser and exit the script. ..")
    browser.close()