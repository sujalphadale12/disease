import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# 1. SETUP HEADLESS BROWSER FOR ONLINE/CLOUD
chrome_options = Options()
chrome_options.add_argument("--headless")  # No GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 2. AUTO-INSTALL DRIVER
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 3. CONNECT TO THE APP
# Use localhost if running in GitHub Actions, or your live .streamlit.app URL
url = os.environ.get("STREAMLIT_URL", "http://localhost:8501")
driver.get(url)

try:
    wait = WebDriverWait(driver, 15)
    
    # Check title
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    assert "Disease Prediction System" in driver.page_source
    print("✅ Title loaded")

    # Select symptom (Updated selector for Streamlit)
    search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label*='symptoms']")))
    search_box.send_keys("Fever")
    search_box.send_keys(Keys.ENTER)
    print("✅ Symptoms selected")

    # Click button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Predict')]")))
    button.click()
    print("✅ Button clicked")

    time.sleep(3)
    if "Predicted Disease" in driver.page_source:
        print("✅ Success: Prediction displayed")
    else:
        print("❌ Failed: Prediction not found")

finally:
    driver.quit()