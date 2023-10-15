import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

# Global dictionary to hold data for each champion
champion_data = {}

def scroll_down(driver, percentage=0.15):
    total_height = driver.execute_script("return document.body.scrollHeight;")
    driver.execute_script(f"window.scrollBy(0, {total_height * percentage});")
    time.sleep(3)  # Pause after scrolling

def extract_runes(driver):
    runes = []
    rune_image_selector = '.row img'
    rune_images = driver.find_elements(By.CSS_SELECTOR, rune_image_selector)

    for img in rune_images:
        src = img.get_attribute('src')
        if 'grayscale' not in src:
            alt = img.get_attribute('alt')
            runes.append(alt)

    return runes

def extract_skills(driver):
    skill_elems = driver.find_elements(By.TAG_NAME, 'strong')
    skills = [elem.text for elem in skill_elems if elem.text in ['Q', 'W', 'E', 'R']]
    return skills[:3]

def op_gg_interaction():
    # Create a Service object
    chrome_service = Service(ChromeDriverManager().install())
    
    # Add options to ignore SSL certificate errors
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    
    # Initialize the Chrome Driver
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    # Navigate to the base URL
    driver.get('https://www.op.gg')
    wait = WebDriverWait(driver, 10)

    for search_term in search_terms:
        time.sleep(3)  # Pause for stability
        
        # Click on the Champions button
        champions_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/champions"]')))
        champions_button.click()

        time.sleep(3)  # Pause to ensure the next page loads properly

        # Use the search bar to find the champion
        search_bar = wait.until(EC.presence_of_element_located((By.ID, 'searchChampion')))
        search_bar.clear()
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

        time.sleep(3)  # Pause after the search

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.row img')))
        
        # Scroll down to see the skill section
        scroll_down(driver)

        # Extract the runes information
        runes = extract_runes(driver)

        # Extract the skill maxing order
        skills = extract_skills(driver)

        # Store the data
        champion_data[search_term] = {'Runes': runes, 'Skills': skills}

    driver.quit()

# Define the search terms
search_terms = ['Viego', 'Yasuo']

# Run the interaction
op_gg_interaction()

# Print the data collected for each champion
for champion, data in champion_data.items():
    print(f'{champion}:')
    for key, value in data.items():
        print(f'  {key}:')
        for item in value:
            print(f'    {item}')
    print()
