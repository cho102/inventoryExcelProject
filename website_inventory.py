#pip install playwright
#playwright install
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("http://192.168.1.12/som/")

    print(page.title())

    browser.close()

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()

#     page.goto("http://192.168.1.12/som/")

#     # Login
#     # ...

#     # Enter SKU
#     page.locator("#ContentPlaceHolder1_TextBoxSKU").fill("FC20600")

#     # Submit
#     page.locator("#ContentPlaceHolder1_ButtonSubmit").click()

#     # Wait for results
#     page.wait_for_load_state("networkidle")

#     print(page.locator("body").inner_text())

#     browser.close()
