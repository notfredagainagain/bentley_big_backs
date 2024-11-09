import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up the Selenium WebDriver
def fetch_menu_with_selenium():
    # Path to your ChromeDriver; adjust as needed
    chrome_driver_path = '/path/to/chromedriver'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    
    # Load the web page
    url = 'https://bentley.sodexomyway.com/en-us/locations/the-921'
    driver.get(url)
    
    # Wait for the page to load (adjust the waiting time if needed)
    time.sleep(5)  # or use WebDriverWait for a more robust solution
    
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
                'tags': tags  # Tags for meal type, nutrition info, etc.
            })
        except AttributeError:
            st.write('Debug: Missing some menu item details')

    return menu_items

# Streamlit app
st.title('The 921 Dietary Suggestions for Your Nutrition Goals')
st.write('Select your nutrition goals and see suitable menu items available.')

# User input for nutrition goals
goal = st.selectbox(
    'Select Your Nutrition Goal',
    ['Weight Loss', 'Muscle Gain', 'Balanced Diet']
)

# User input for dietary preferences (optional)
preferences = st.multiselect(
    'Dietary Preferences (optional)',
    ['Vegetarian', 'Vegan', 'Gluten-Free', 'Halal', 'Kosher', 'Nut-Free', 'Dairy-Free']
)

# Fetch and display the menu
if st.button('Show Menu'):
    menu_items = fetch_menu_with_selenium()
    
    # Filter based on the nutrition goal
    filtered_menu = [item for item in menu_items if any(goal.lower() in item['tags'].lower() for goal in preferences)]
    
    # Display filtered results
    if filtered_menu:
        for item in filtered_menu:
            st.subheader(item['name'])
            st.write(item['description'])
            st.write(f"**Allergens:** {item['allergens']}")
            st.write(f"**Tags:** {item['tags']}")
    else:
        st.write('No menu items match your nutrition goals and dietary preferences.')
