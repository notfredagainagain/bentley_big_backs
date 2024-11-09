import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Use `chromium`, `firefox`, or `webkit`
        context = await browser.new_context()
        page = await context.new_page()

        # Replace this URL with the target URL
        url = "https://example.com"
        await page.goto(url)

        # Get the page content
        content = await page.content()

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Example extraction logic (adjust as needed)
        menu_items = soup.find_all("div", class_="Menustyles__MenuMealSection-sc-eo2633-2")
        data = []
        for item in menu_items:
            header = item.find("h2")
            if header:
                data.append(header.text)

        # Create a DataFrame and print the extracted data
        df = pd.DataFrame(data, columns=["Menu Items"])
        print(df)

        # Close the browser
        await browser.close()

# Run the async function
asyncio.run(main())
