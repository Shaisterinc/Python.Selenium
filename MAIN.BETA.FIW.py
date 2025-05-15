import os
import datetime 
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

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    filename='PM.LOG.FIW.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---- CONFIGURATION ----
URL = "https://www.popmart.com/us/products/1061/THE-MONSTERS-FALL-IN-WILD-SERIES-Vinyl-Plush-Doll-Pendant"
BUTTON_XPATH = '//div[contains(text(), "ADD TO BAG") and (contains(@class, "index_usBtn") or contains(@class, "index_btnFull"))]'
COOKIE_XPATH = '//div[contains(text(), "ACCEPT") and contains(@class, "policy_acceptBtn")]'
CHROME_DRIVER_PATH = "/Users/treysongz/Selenium/chromedriver"
EMAIL_FROM = "try.shai.im@gmail.com"
EMAIL_PASSWORD = "emxq worj nzoa kubp"
EMAIL_TO = ["try@cogosystems.com", "duyenan88@hotmail.com"]
WAIT_TIMEOUT = 20
# ------------------------

def send_email(subject: str, body: str, success_log: str = None, error_log: str = None):
    """Generic email sending function supporting multiple recipients."""
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = ", ".join(EMAIL_TO)  # Join list into comma-separated string

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
        if success_log:
            logging.info(success_log)
    except Exception as e:
        if error_log:
            logging.error(f"{error_log}: {e}")

def send_email_click_pay():
    send_email(
        subject="Proceed to Pay Successful",
        body="Successfully Proceeded to Pay.",
        success_log="✅ Success Email Sent on Proceed to Pay",
        error_log="❌ Failed to send success email"
    )

def send_email_noclick_pay():
    send_email(
        subject="Proceed to Pay Failed",
        body="Failed to Proceed to Pay.",
        success_log="⚠️ Failure Email Sent on Proceed to Pay",
        error_log="❌ Failed to send failure email"
    )

def send_email_avail():
    send_email(
        subject="POP MART Item Available",
        body=(
            "🎉 The item is available to add to the bag:\n\n"
            "Product: THE MONSTERS Big into Energy Series-Vinyl Plush Pendant Blind Box\n"
            f"URL: {URL}\n\n"
            "You can now proceed to purchase.\n"
            "Go get it before it’s gone!"
        ),
        success_log="📦 Email for availability sent",
        error_log="❌ Failed to send availability email"
    )

def send_email_unavail():
    send_email(
        subject="POP MART Item Not Available",
        body=(
            "😔 The following item is NOT available:\n\n"
            "Product: THE MONSTERS Big into Energy Series-Vinyl Plush Pendant Blind Box\n"
            f"URL: {URL}\n\n"
            "Please check back later."
        ),
        success_log="📭 Email for unavailability sent",
        error_log="❌ Failed to send unavailability email"
    )

def send_email_payment_ok(subject, message):
    send_email(subject, message)

def send_email_payment_notok():
    send_email("❌ Payment Failed", "There was an error during the payment process. Please check the logs or screenshot for more details.")

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
# print("✅ Starting automation flow")
def automate_selections(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)

    def force_select(label):
        try:
            print(f"Selecting: {label}")
            element_xpath = f"//div[text()='{label}']"
            selected_xpath = f"{element_xpath}[contains(@class, 'index_activeSizeTitle__QNbgr')]"

            element = wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
            element.click()
            print(f"✅ Clicked: {label}")

            wait.until(EC.presence_of_element_located((By.XPATH, selected_xpath)))
            print(f"Confirmed '{label}' is selected.")
            time.sleep(1.2)
        except Exception as e:
            print(f"❌ Failed to select {label}: {e}")

    def add_to_bag():
        try:
            print("Clicking 'ADD TO BAG'...")
            btn_xpath = "//div[text()='ADD TO BAG']"
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
            btn.click()
            print("Item added to bag.")
            time.sleep(3)            
        except Exception as e:
            print(f"Failed to add to bag: {e}")

    def is_cart_empty():
        try:
            # This logic may vary — adjust if needed
            cart_icon = driver.find_element(By.XPATH, "//img[contains(@src, 'bag.png')]")
            if cart_icon:
                print("Something already in cart.")
                return False
        except:
            print("Cart appears empty.")
            return True

        return True

    # ✅ Only add "Single box" if nothing is in cart
    if is_cart_empty():
        force_select("Single box")
        add_to_bag()
    else:
        print("❗Skipping 'Single box' — already in cart.")

    # ✅ Always add "Whole set"
    force_select("Whole set")
    add_to_bag()
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
        phone.send_keys("714-309-2559")

        # Address
        address = wait.until(EC.presence_of_element_located((By.ID, "detailInfo")))
        address.clear()
        address.send_keys("10081 Beverly Lane")

        # City
        city = wait.until(EC.presence_of_element_located((By.ID, "cityName")))
        city.clear()
        city.send_keys("Westminster")

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
        zip_code.send_keys("92683")

        # Save
        save_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class, 'addressSave') and text()='Save']"
        )))
        save_button.click()
        logging.info("Clicked: Save address")     
        time.sleep(3)

    except Exception as e:
        logging.info(f"❌ Error while filling address form: {e}")       
# ---------------------------

def click_again(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)

    # Step 1: Click "Edit" button
    try:
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='Edit' and contains(@class,'index_editBtn__DlxPQ')]"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", edit_btn)
        logging.info("✅ Clicked Edit button")        
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
        ))).send_keys("4100390642368266")
        driver.switch_to.default_content()

        # === EXPIRY DATE ===
        driver.switch_to.frame(iframes[1])
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedExpiryDate']"
        ))).send_keys("07/25")
        driver.switch_to.default_content()

        # === CVC ===
        driver.switch_to.frame(iframes[2])
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedSecurityCode']"
        ))).send_keys("558")
        driver.switch_to.default_content()

        # === NAME ON CARD ===
        name_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.NAME, "holderName"))
        )
        name_input.clear()
        name_input.send_keys("Try Im")       

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
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = "Screenshots"
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/Payment_Screenshot_{timestamp}.png"
        driver.save_screenshot(filename)        

        # ✅ Send success email with total
        send_email_payment_ok("💳 Payment Successful", f"Payment submitted successfully.\n\nAmount: {total_text}")

    except Exception as e:
        logging.info(f"❌ Error during payment process: {e}")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = "Screenshots"
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/Payment_Error_screenshot_{timestamp}.png"
        driver.save_screenshot(filename)        
        send_email_payment_notok()
# ---------------------------

def check_product():
    print("Launching browser...")
    logging.info("Starting script...")

    driver = None
    try:
        # Set up Chrome options
        options = uc.ChromeOptions()               
        options.add_argument("--no-sandbox") 
        options.add_argument("--disable-gpu")       
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-extensions")      
        
        CHROME_BROWSER_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"        
        CHROME_DRIVER_PATH = "C:/Users/admin/Selenium/chromedriver.exe"  

        options.binary_location = CHROME_BROWSER_PATH 

        uc.Chrome.__del__ = lambda self: None      
                                            
        driver = uc.Chrome(options=options,                                   
        # browser_executable_path=CHROME_BROWSER_PATH,
        version_main=136,
        use_subprocess=False,
        driver_executable_path=CHROME_DRIVER_PATH)

                # Set the window size to half of the screen
        screen_width = 1920
        screen_height = 1080

        half_width = screen_width // 2
        half_height = screen_height // 2

        driver.set_window_position(half_width, half_height) 
        driver.set_window_size(half_width, half_height)

        start_time = time.time()
        driver.get(URL)  # Your target URL here
        time.sleep(3)  # Wait for page load or replace with better wait

        # Accept cookies if popup is presentdef send_email(subject, message):
        accept_cookies_if_present(driver)

        driver.implicitly_wait(10)

        wait = WebDriverWait(driver, 20)
        try:

            add_to_bag_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, BUTTON_XPATH))
            )

            print("ADD TO BAG' button is available.")
            
            # Click the button if needed
            driver.execute_script("arguments[0].click();", add_to_bag_button)

            # Send email for availability
            send_email_avail()
            print("Email for availability sent. Continuing with script...")
            logging.info("📧 Email for availability sent. Continuing with script...")
            
        except TimeoutException:
            logging.info("❌ 'ADD TO BAG' button not found. Stopping script.")                        
            # Optionally send a different email if it's not found
            # send_email_unavail() 
            return   


        # Automate product selections
        automate_selections(driver)

        # Click the shopping bag icon to view cart
        click_shopping_bag_icon(driver)

        # Quick scroll
        quick_scroll(driver)

        # Click check box to select all items
        click_custom_checkbox(driver)

        # Click the CHECK OUT button
        checkout(driver)

        # Click CHECKOUT AS GUEST
        click_checkout_as_guest(driver)

        # Enter email and confirm
        enter_email_and_confirm(driver)

        # Add new address
        click_add_new_address(driver)

        # Enter address manually
        click_enter_address_manually(driver)

        # Fill address form
        fill_address_form(driver)

        # Possibly click again for address confirmation (if needed)
        click_again(driver)

        # Proceed to pay
        click_proceed_to_pay(driver)

        # Fill credit card info and pay
        fill_credit_card_and_pay(driver)

        logging.info("Script completed successfully.")

    except Exception as e:
        logging.error(f"Unexpected error in main flow: {e}", exc_info=True)
            
       
    finally:
        print("Closing browser...")
        if driver is not None:
            driver.quit()
            
if __name__ == "__main__":
    check_product()
