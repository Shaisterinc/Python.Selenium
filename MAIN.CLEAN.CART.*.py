"""
Author: Trey Songz
Date: 2025-04-04
Description: 
    - Automates checking product availability on the POP MART website.
    - Sends email notifications based on availability.
    - Automates the checkout process, including address and payment information.
Technologies:
    - Python Version: 3.12.0
    - Selenium Version: 4.21.0
    - Undetected ChromeDriver Version: 3.2.0
"""
# ------------------------
import sys
import time
import random
import logging
import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc

# Configure logging
logging.basicConfig(
    filename='CLEAN.CART.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s")

CHROME_DRIVER_PATH = "/Users/treysongz/Selenium/chromedriver"
WAIT_TIMEOUT = 20

def cleanup_cart():
    print("🚀 Launching browser...")
    logging.info("Starting script...")

    driver = None

    #---- ADD TO BAG AND VIEW CART FUNCTIONS ----
    def click_shopping_bag_icon(driver):
        try:
            # Wait for the image to appear
            img = WebDriverWait(driver, timeout=WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, "//img[@alt='POP MART' and contains(@src, 'bag.png')]"))
            )

            # Get its clickable parent (e.g. a button or anchor tag)
            clickable_parent = img.find_element(By.XPATH, "./ancestor::*[self::a or self::button or self::div][1]")

            # Scroll into view and click
            driver.execute_script("arguments[0].scrollIntoView(true);", clickable_parent)
            clickable_parent.click()
            logging.info("🛍️ Clicked shopping bag icon.")
        
        except Exception as e:
            logging.info(f"❌ Failed to click shopping bag icon: {e}")
            raise

    try:
        # Set up Chrome options 
        CHROME_BROWSER_PATH = "/Applications/Google Chrome 124/Google Chrome.app/Contents/MacOS/Google Chrome"        
        CHROME_DRIVER_PATH = "/Users/treysongz/Selenium/chromedriver"
           
        options = uc.ChromeOptions()               
        options.add_argument("--no-sandbox")        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--user-data-dir=/tmp/my-unique-profile")  

        options.binary_location = CHROME_BROWSER_PATH        
                                             
        driver = uc.Chrome(options=options, 
        Version_main=124,                     
        browser_executable_path=CHROME_BROWSER_PATH,
        use_subprocess=False,
        driver_executable_path=CHROME_DRIVER_PATH)

        # Set the window size to half of the screen
        screen_width = 2560
        screen_height = 1080

        half_width = screen_width // 2
        half_height = screen_height // 2

        driver.set_window_position(0, half_height)  
        driver.set_window_size(half_width, half_height)      
            
        start_time = time.time()    
    
        driver.get("https://www.popmart.com/us/products/2209/Twinkle-Twinkle-Be-a-Little-Star-Series-Figures")

        click_shopping_bag_icon(driver)

        timeout = 20
        try:
            # Wait and click the checkbox
            checkbox = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'index_checkbox__w_166'))
            )
            checkbox.click()
            logging.info("✅ Clicked custom checkbox.")
        except Exception as e:
            logging.info(f"❌ Failed to click checkbox: {e}")
            return
        
        try:
            # Wait and click the remove button
            remove_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'product_remove__Oiza1'))
            )
            remove_button.click()
            logging.info("✅ Clicked remove button.")

        except Exception as e:
            logging.info(f"❌ Failed to click remove button: {e}")
            return
    finally:
        print("🧹 Closing browser...")
        time.sleep(3)
        if driver is not None:
            driver.quit()
        logging.info("🧹 Browser closed after clean-up.")

if __name__ == "__main__":
    cleanup_cart()
