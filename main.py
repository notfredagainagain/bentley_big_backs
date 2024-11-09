import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller  # New import
from bs4 import BeautifulSoup
import time

# Automatically download and set up ChromeDriver
chromedriver_autoinstaller.install()

# Function to fetch and parse the daily menu
def fetch_menu_with_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode for server environments
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Set up the WebDriver
    driver = webdriver.Chrome(options=options)
    
    # Load the web page
    url = 'https://bentley.sodexomyway.com/en-us/locations/the-921'
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)
    
    # Get the page source and pass it to BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Close the driver
    driver.quit()
    
    # Debug: Print the page content
    st.write('Debug: Full page content preview', soup.prettify()[:1000])

    menu_items = []
    for item in soup.find_all('div', class_='menu-item'):  # Adjust the class name as needed
        try:
            name = item.find('div', class_='menu-item-name').text.strip()
            description = item.find('div', class_='menu-item-description').text.strip()
            allergens = item.find('div', class_='menu-item-allergens').text.strip()
            tags = item.find('div', class_='menu-item-tags').text.strip()  # Adjust as needed
            menu_items.append({
                'name': name,
                'description': description,
                'allergens': allergens,
                'tags': tags
            })
        except AttributeError:
            st.write('Debug: Missing some menu item details')

    return menu_items
