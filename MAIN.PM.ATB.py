# Author: Trey Songz
# Date: 2025-04-04  
# Description: This script automates the process of checking the availability of a product on the POP MART website. 
# It sends email notifications based on its availability. 
# It also automates the checkout process, including filling out address and payment information.
# The script is designed to work with the POP MART website and uses Selenium for web automation.
# It uses Selenium for web automation and smtplib for sending emails.
# Python Version: 3.12.0
# Selenium Version: 4.21.0
# Undetected ChromeDriver Version: 3.2.0
# ------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from email.message import EmailMessage
import undetected_chromedriver as uc
import smtplib
import sys  
import time 
import random
import logging

logging.basicConfig(
    filename='PM.LOG.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---- CONFIGURATION ----
URL = "https://www.popmart.com/us/products/2209/Twinkle-Twinkle-Be-a-Little-Star-Series-Figures"
BUTTON_XPATH = '//div[contains(text(), "ADD TO BAG") and (contains(@class, "index_usBtn") or contains(@class, "index_btnFull"))]'
COOKIE_XPATH = '//div[contains(text(), "ACCEPT") and contains(@class, "policy_acceptBtn")]'
CHROME_DRIVER_PATH = "/Users/treysongz/Selenium/chromedriver"
EMAIL_FROM = "try.shai.im@gmail.com"
EMAIL_PASSWORD = "emxq worj nzoa kubp"  # Use App Password
EMAIL_TO = ["try@cogosystems.com", "duyenan88@hotmail.com"]
WAIT_TIMEOUT = 20
# ------------------------

# ---- EMAIL FUNCTIONS Click FULL PAY ----
def send_email_payment_ok(subject, content):
    msg = EmailMessage()
    msg.set_content("💳 Payment Successfully Processed.\n"
                    "There were no errors during payment.\\n"
                    "Amount: {total_text}")
    msg["Subject"] = "Payment Successful"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Payment Email Sent.")
    except Exception as e:
        logging.info(f"❌ Failed to send payment email: {e}")
        
def send_email_payment_notok(subject, content):
    msg = EmailMessage()
    msg.set_content("❌ Payment Failed to Process.\n"
                    "There was an error during payment.")
    msg["Subject"] = "Payment Failed"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logging.info("Payment Email Sent.")            
    except Exception as e:
        logging.info(f"❌ Failed to send payment email: {e}")
# ------------------------

# ---- EMAIL FUNCTIONS Click Proceed to PAY----
def send_email_click_pay(subject, content):
    msg = EmailMessage()
    msg.set_content("Successully Proceeded to Pay.")
    msg["Subject"] = "Proceed to Pay Successful"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logging.info("Success Email Sent on Proceed to Pay.")            
    except Exception as e:
        logging.info(f"❌ Failed to send success email: {e}")       

def send_email_noclick_pay(subject, content):
    msg = EmailMessage()
    msg.set_content("Failed to Proceed to Pay.")
    msg["Subject"] = "Proceed to Pay Failed"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logging.info("Failure Email Sent on Proceed to Pay.")            
    except Exception as e:
        logging.info(f"❌ Failed to send failure email: {e}")       
# ------------------------

# ---- EMAIL FUNCTIONS Item Available----
def send_email_avail():
    msg = EmailMessage()
    msg.set_content("🎉 The item is available to add to the bag:\n\n"
                    "Product: THE MONSTERS - I FOUND YOU Vinyl Face Doll\n"
                    "URL: https://www.popmart.com/us/products/878/THE-MONSTERS---I-FOUND-YOU-Vinyl-Face-Doll\n\n"
                    "You can now proceed to purchase.\n"
                    "Go get it before it’s gone!")
    msg["Subject"] = "POP MART Item Available"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logging.info("Email for availability sent.")            
    except Exception as e:
        logging.info(f"❌ Failed to send availability email: {e}")        

def send_email_unavail():
    msg = EmailMessage()
    msg.set_content("😔 The following item is NOT available:\n\n"
                    "Product: THE MONSTERS - I FOUND YOU Vinyl Face Doll\n"
                    "URL: https://www.popmart.com/us/products/878/THE-MONSTERS---I-FOUND-YOU-Vinyl-Face-Doll\n\n"
                    "Please check back later.")
    msg["Subject"] = "POP MART Item Not Available"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            logging.info("Email for unavailability sent.")            
    except Exception as e:
        logging.info(f"❌ Failed to send unavailability email: {e}")        
# ------------------------
 
# ---- FUNCTIONS ---- 
# Function to accept cookies if the popup is present
def accept_cookies_if_present(driver, timeout=WAIT_TIMEOUT):
    try:
        accept_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, COOKIE_XPATH))
        )
        driver.execute_script("arguments[0].click();", accept_button)
        logging.info("Accepted cookie/privacy popup.")
    except TimeoutException:
        logging.info("No cookie/privacy popup to accept.")
# ---------------------------    

# ---- PRODUCT SELECTION ----
def wait_and_add_to_bag(driver, timeout=WAIT_TIMEOUT):
    wait = WebDriverWait(driver, timeout)

    try:
        logging.info("🔍 Looking for 'ADD TO BAG' button...")
        btn_xpath = "//div[text()='ADD TO BAG']"
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
        btn.click()
        logging.info("✅ Clicked 'ADD TO BAG'!")
        time.sleep(3)  # Optional delay to let the action complete
    except Exception as e:
        logging.info(f"❌ Could not click 'ADD TO BAG': {e}")
# ---------------------------
    
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
#   ---------------------------

def quick_scroll(driver, timeout=5, step=500, pause=0.01):
    start_time = time.time()
    while True:
        driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(pause)
        current_offset = driver.execute_script("return window.pageYOffset + window.innerHeight;")
        total_height = driver.execute_script("return document.body.scrollHeight")
        if current_offset >= total_height or time.time() - start_time > timeout:
            break

# ---- CUSTOM CHECKBOX FUNCTIONS ----
def click_custom_checkbox(driver, timeout=WAIT_TIMEOUT):
    try:
        checkbox = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'index_checkbox__w_166'))
        )
        checkbox.click()
        logging.info("✅ Clicked custom checkbox.")        
    except Exception as e:
        logging.info(f"❌ Failed to click checkbox: {e}")               

def checkout(driver, timeout=WAIT_TIMEOUT):
    try:        
        # Step 1: Click the CHECK OUT button
        checkout_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "ant-btn") and contains(@class, "ant-btn-primary") and contains(@class, "index_checkout__V9YPC") and contains(text(), "CHECK OUT")]'))
        )
        driver.execute_script("arguments[0].click();", checkout_button)
        logging.info("Clicked: CHECK OUT button")       
    except TimeoutException:
        logging.info("❌ 'CHECK OUT' button not found.")        
# ---------------------------

# ---- CHECKOUT FUNCTIONS ----
def click_checkout_as_guest(driver, timeout=WAIT_TIMEOUT):
    wait = WebDriverWait(driver, timeout)

    try:
        # Wait for the "CHECKOUT AS GUEST" span to appear and be clickable
        guest_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='CHECKOUT AS GUEST']"
        )))
        guest_button.click()
        logging.info("Clicked: CHECKOUT AS GUEST")        
        time.sleep(2)  # Wait for next step to load
    except Exception as e:
        logging.info(f"❌ Error clicking CHECKOUT AS GUEST: {e}")        
# ---------------------------

# ---- EMAIL CONFIRMATION FUNCTIONS ----
def enter_email_and_confirm(driver, timeout=WAIT_TIMEOUT):
    wait = WebDriverWait(driver, timeout)
    email = "tr.sh.i@gmail.com"

    try:
        # Step 1: Enter email
        email_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@placeholder='Enter your email']"
        )))
        email_input.clear()
        email_input.send_keys(email)
        logging.info(f"Entered email: {email}")        
        time.sleep(1)

        # Step 2: Click the first "CONFIRM" button
        confirm_btn1 = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[contains(@class,'index_applyBtn__') and text()='CONFIRM']"
        )))
        confirm_btn1.click()
        logging.info("Clicked first CONFIRM button")
        time.sleep(2) # Wait for the next step to load

        # Step 3: Click the second "CONFIRM" button        
        WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((
            By.XPATH, "//button[.//span[text()='CONFIRM']]"
        )))
        
        confirm_btn2 = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[text()='CONFIRM']]"
        )))
        confirm_btn2.click()
        logging.info("Clicked second CONFIRM button")        
        time.sleep(2)
   
    except Exception as e:
        logging.info(f"❌ Error during email confirmation: {e}")        
# ---------------------------

# ---- ADDRESS FUNCTIONS ----
def click_add_new_address(driver, timeout=WAIT_TIMEOUT):
    wait = WebDriverWait(driver, timeout)
    try:
        # Use XPath with exact text match
        add_address_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[normalize-space(text())='Add a new address']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", add_address_btn)
        add_address_btn.click()
        logging.info("Clicked: Add a new address")        
        time.sleep(2)
    except Exception as e:
        logging.info(f"❌ Error clicking Add a new address: {e}")   
# ---------------------------

# ---- MANUAL ADDRESS ENTRY FUNCTIONS ----
def click_enter_address_manually(driver, timeout=WAIT_TIMEOUT):
    wait = WebDriverWait(driver, timeout)
    try:
        manual_entry_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='Enter it manually' and contains(@class, 'addOrUpdateAddress_text__')]"
        )))
        manual_entry_btn.click()
        logging.info("Clicked: Enter it manually")        
        time.sleep(1.5)
    except Exception as e:
        logging.info(f"❌ Error clicking 'Enter it manually': {e}")        
# ---------------------------

# ---- ADDRESS FORM FILLING FUNCTIONS ----
def fill_address_form(driver, timeout=WAIT_TIMEOUT):
    wait = WebDriverWait(driver, timeout)

    try:
        # First Name
        first_name = wait.until(EC.presence_of_element_located((By.ID, "givenName")))
        first_name.clear()
        first_name.send_keys("Try")

        # Last Name
        last_name = wait.until(EC.presence_of_element_located((By.ID, "familyName")))
        last_name.clear()
        last_name.send_keys("Im")

        # Phone Number
        phone = wait.until(EC.presence_of_element_located((By.ID, "telNumber")))
        phone.clear()
        phone.send_keys("714-258-2889")

        # Address
        address = wait.until(EC.presence_of_element_located((By.ID, "detailInfo")))
        address.clear()
        address.send_keys("3455 Comer Ave")

        # City
        city = wait.until(EC.presence_of_element_located((By.ID, "cityName")))
        city.clear()
        city.send_keys("Riverside")

        # Province / State Dropdown
        province_input = wait.until(EC.presence_of_element_located((By.ID, "province")))
        province_input.click()
        
        time.sleep(1)

        california_option = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@class='ant-select-item-option-content' and text()='California']"
        )))
        california_option.click()        
        time.sleep(1)

        # Zip Code
        zip_code = wait.until(EC.presence_of_element_located((By.ID, "postalCode")))
        zip_code.clear()
        zip_code.send_keys("92507")

        # Save
        save_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class, 'addressSave') and text()='Save']"
        )))
        save_button.click()
        logging.info("Clicked: Save address")     
        time.sleep(2)

    except Exception as e:
        logging.info(f"❌ Error while filling address form: {e}")       
# ---------------------------

def click_again(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)

    # Step 1: Click "Edit" button
    try:
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='Edit' and contains(@class,'index_editBtn__')]"
        )))
        time.sleep(2)
        edit_btn.click()        
    except Exception as e: 
        logging.info(f"❌ Error clicking Edit button: {e}")       
        return

    # Step 2: Click first "CONFIRM" button with class
    try:
        confirm_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='CONFIRM' and contains(@class,'index_applyBtn__')]"
        )))
        confirm_btn.click()        
    except Exception as e:     
        logging.info(f"❌ Error clicking first CONFIRM button: {e}")   
        return

    # Step 3: Click second "CONFIRM" button (generic)
    try:
        confirm_btn2 = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[normalize-space(text())='CONFIRM']]"
        )))
        confirm_btn2.click()        
    except Exception as e:
        logging.info(f"❌ Error clicking second CONFIRM button: {e}")
        return
    logging.info("Clicked: CONFIRM button")
    time.sleep(5)  # Wait for the next step to load      

# ---- PROCEED TO PAY FUNCTIONS ----
def click_proceed_to_pay(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        proceed_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class, 'index_placeOrderBtn__') and text()='PROCEED TO PAY']"
        )))
        driver.execute_script("arguments[0].click();", proceed_btn)  # Use JS click as a backup
        print("Clicked: PROCEED TO PAY")
        driver.save_screenshot("proceed_to_pay_screenshot.png")  # Screenshot for verification
        time.sleep(5)

        # ✅ Success email
        send_email_click_pay("Checkout Successful", "The checkout proceeded successfully.")

    except TimeoutException as e:

        # ❌ Failure email
        driver.save_screenshot("proceed_to_pay_error_screenshot.png")  # Screenshot for verification
        send_email_noclick_pay("Checkout Failed", f"There was an error during checkout: {e}")

# ---------------------------

#---- PAYMENT FUNCTIONS ----
def fill_credit_card_and_pay(driver, timeout=WAIT_TIMEOUT):
    wait = WebDriverWait(driver, timeout)
    try:
        # 1. Click credit card radio button
        credit_card_option = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class, 'index_payIcon__') and .//img[contains(@src, 'credit_card')]]"
        )))
        driver.execute_script("arguments[0].click();", credit_card_option)  # JS click for reliability
        logging.info("Clicked: Credit Card Option")
                
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "iframe[name*='encryptedCardNumber'], iframe.js-iframe")
        ))
        time.sleep(5) # Wait for iframes to load
        
        # 2. Enter credit card info (inside iframes)

        # Wait for all Adyen iframes to load
        iframes = WebDriverWait(driver, timeout).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "iframe.js-iframe")
        )

        # ⚠️ Confirm we have all 3 required fields
        if len(iframes) < 3:
            raise Exception("Less than 3 Adyen iframes found")

        # === CARD NUMBER ===
        driver.switch_to.frame(iframes[0])
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedCardNumber']"
        ))).send_keys("1234567898652145")
        driver.switch_to.default_content()

        # === EXPIRY DATE ===
        driver.switch_to.frame(iframes[1])
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedExpiryDate']"
        ))).send_keys("01/29")
        driver.switch_to.default_content()

        # === CVC ===
        driver.switch_to.frame(iframes[2])
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedSecurityCode']"
        ))).send_keys("222")
        driver.switch_to.default_content()

        # === NAME ON CARD ===
        name_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.NAME, "holderName"))
        )
        name_input.clear()
        name_input.send_keys("John Doe")       

        # 4. Capture total amount from Pay button
        pay_btn = wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[contains(@class, 'adyen-checkout__button--pay')]"
        )))
        total_text = pay_btn.text  # Example: "Pay $26.79"
        print(f"Total amount to pay: {total_text}")
        logging.info(f"Total amount to pay: {total_text}")
        
        # 5. Click the Pay button
        pay_btn.click()
        logging.info("Clicked: Pay button")
        time.sleep(5)  # Wait for payment processing
        driver.save_screenshot("payment_screenshot.png")  # Screenshot for verification

        # ✅ Send success email with total
        send_email_payment_ok("💳 Payment Successful", f"Payment submitted successfully.\n\nAmount: {total_text}")

    except Exception as e:
        logging.info(f"❌ Error during payment process: {e}")
        driver.save_screenshot("payment_error_screenshot.png")  # Screenshot for verification
        send_email_payment_notok()
# ---------------------------

# ---- MAIN FUNCTION ----
def check_product():
    print("🚀 Launching browser...")
    logging.info("Starting script...")
    
    driver = None
  
    try:
        # Set up Chrome options        
        options = uc.ChromeOptions()
        options.headless = False
        options.add_argument("--start-standalone")        
        options.add_argument("--no-sandbox")        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")                   
                        
        driver = uc.Chrome(version_main=124, options=options)
        
        driver.get(URL)
        accept_cookies_if_present(driver)

        try:
            add_to_bag_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, BUTTON_XPATH))
            )

            print("✅ 'ADD TO BAG' button is available.")
            
            # Click the button if needed
            driver.execute_script("arguments[0].click();", add_to_bag_button)

            # Send email for availability
            send_email_avail()
            print("📧 Email for availability sent. Continuing with script...")
            logging.info("📧 Email for availability sent. Continuing with script...")
            
        except TimeoutException:
            logging.info("❌ 'ADD TO BAG' button not found. Stopping script.")                        
            # Optionally send a different email if it's not found
            # send_email_unavail() 
            return             
        
        wait_and_add_to_bag(driver)
        click_shopping_bag_icon(driver)        
        click_custom_checkbox(driver)        
        quick_scroll(driver)       
        checkout(driver)     
        click_checkout_as_guest(driver)       
        enter_email_and_confirm(driver)        
        click_add_new_address(driver)      
        click_enter_address_manually(driver)    
        fill_address_form(driver)     
        click_again(driver)        
        click_proceed_to_pay(driver)     
        fill_credit_card_and_pay(driver)
        time.sleep(2)

        print("🧪 Keeping browser open for observation...")
        time.sleep(5)  # Adjust or remove as needed       
       
    
    finally:
        print("🧹 Closing browser...")
        if driver is not None:
            driver.quit()
            
if __name__ == "__main__":
    check_product()
