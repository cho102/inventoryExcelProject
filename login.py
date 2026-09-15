from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    context = browser.new_context()

    page = context.new_page()

    # Open the inventory website
    page.goto("http://192.168.1.12/som/")

    # Log in manually
    print("Please log in to the inventory website.")
    input("After you finish logging in, press Enter here...")

    # Save the login session
    context.storage_state(path="login_state.json")

    print("Login session saved!")

    browser.close()
