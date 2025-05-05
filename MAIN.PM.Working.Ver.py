# Author: Trey Songz
# Date: 2024-01-01  
# Description: This script automates the process of checking the availability of a product on the POP MART website. 
# It sends email notifications based on its availability. 
# It uses Selenium for web automation and smtplib for sending emails.
# Python Version: 3.12.0
# Selenium Version: 4.21.0
# ------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
import sys   # For exit codes
import time  # For sleep
import random
from email.message import EmailMessage

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

# ---- EMAIL FUNCTIONS ----
def send_email_click_pay(subject, content):
    msg = EmailMessage()
    msg.set_content("Successully proceeded to pay.")
    msg["Subject"] = "Proceed to Pay Successful"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Success Email Sent on Proceed to Pay.")
    except Exception as e:
        print(f"❌ Failed to send success email: {e}")

def send_email_noclick_pay(subject, content):
    msg = EmailMessage()
    msg.set_content("Failed to proceed to pay.")
    msg["Subject"] = "Proceed to Pay Failed"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Failure Email Sent on Proceed to Pay.")
    except Exception as e:
        print(f"❌ Failed to send failure email: {e}")
# ------------------------

# ---- EMAIL FUNCTIONS ----
def send_email_avail():
    msg = EmailMessage()
    msg.set_content("🎉 The item is available to add to the bag:\n\n"
                    "Product: THE MONSTERS Big into Energy Series-Vinyl Plush Pendant Blind Box\n"
                    "URL: https://www.popmart.com/us/products/2155/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box\n\n"
                    "You can now proceed to purchase.\n"
                    "Go get it before it’s gone!")
    msg["Subject"] = "POP MART Item Available"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email for availability sent.")
    except Exception as e:
        print(f"Error sending email: {e}")

def send_email_unavail():
    msg = EmailMessage()
    msg.set_content("😔 The following item is NOT available:\n\n"
                    "Product: THE MONSTERS Big into Energy Series-Vinyl Plush Pendant Blind Box\n"
                    "URL: https://www.popmart.com/us/products/2155/THE-MONSTERS-Big-into-Energy-Series-Vinyl-Plush-Pendant-Blind-Box\n\n"
                    "Please check back later.")
    msg["Subject"] = "POP MART Item Not Available"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email for unavailability sent.")
    except Exception as e:
        print(f"Error sending email: {e}")
# ------------------------
 
# ---- FUNCTIONS ---- 
# Function to accept cookies if the popup is present
def accept_cookies_if_present(driver):
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, COOKIE_XPATH))
        )
        driver.execute_script("arguments[0].click();", accept_button)
        print("✅ Accepted cookie/privacy popup.")
    except TimeoutException:
        print("No cookie/privacy popup to accept.")
# ---------------------------        


# ---- PRODUCT SELECTION ----
# print("✅ Starting automation flow")
def automate_selections(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)

    def force_select(label):
        try:
            print(f"🔍 Selecting: {label}")
            element_xpath = f"//div[text()='{label}']"
            selected_xpath = f"{element_xpath}[contains(@class, 'index_activeSizeTitle__QNbgr')]"

            element = wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
            element.click()
            print(f"✅ Clicked: {label}")

            wait.until(EC.presence_of_element_located((By.XPATH, selected_xpath)))
            print(f"🎯 Confirmed '{label}' is selected.")
            time.sleep(1.2)
        except Exception as e:
            print(f"❌ Failed to select {label}: {e}")

    def add_to_bag():
        try:
            print("🛒 Clicking 'ADD TO BAG'...")
            btn_xpath = "//div[text()='ADD TO BAG']"
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
            btn.click()
            print("✅ Item added to bag.")
            time.sleep(3)            
        except Exception as e:
            print(f"❌ Failed to add to bag: {e}")

    def is_cart_empty():
        try:
            # This logic may vary — adjust if needed
            cart_icon = driver.find_element(By.XPATH, "//img[contains(@src, 'bag.png')]")
            if cart_icon:
                print("🛍️ Something already in cart.")
                return False
        except:
            print("🧺 Cart appears empty.")
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


    print("🧭 Done with automate_selections.")
    print("🧪 About to screenshot after auto select")    
# ---------------------------

    
#---- ADD TO BAG AND VIEW CART FUNCTIONS ----
def click_shopping_bag_icon(driver):
    try:
        # Wait for the image to appear
        img = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[@alt='POP MART' and contains(@src, 'bag.png')]"))
        )

        # Get its clickable parent (e.g. a button or anchor tag)
        clickable_parent = img.find_element(By.XPATH, "./ancestor::*[self::a or self::button or self::div][1]")

        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView(true);", clickable_parent)
        clickable_parent.click()
        print("🛍️ Clicked shopping bag icon.")
    
    except Exception as e:
        print(f"❌ Failed to click shopping bag icon: {e}")
        raise
#   ---------------------------

def quick_scroll(driver, timeout=4, step=500, pause=0.01):
    start_time = time.time()
    while True:
        driver.execute_script(f"window.scrollBy(0, {step});")
        time.sleep(pause)
        current_offset = driver.execute_script("return window.pageYOffset + window.innerHeight;")
        total_height = driver.execute_script("return document.body.scrollHeight")
        if current_offset >= total_height or time.time() - start_time > timeout:
            break

# ---- CUSTOM CHECKBOX FUNCTIONS ----
def click_custom_checkbox(driver, timeout=10):
    try:
        checkbox = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'index_checkbox__w_166'))
        )
        checkbox.click()
        print("Checkbox clicked.")
    except Exception as e:
        print(f"Failed to click checkbox: {e}")        

def checkout(driver):
    try:        
        # Step 1: Click the CHECK OUT button
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "ant-btn") and contains(@class, "ant-btn-primary") and contains(@class, "index_checkout__V9YPC") and contains(text(), "CHECK OUT")]'))
        )
        driver.execute_script("arguments[0].click();", checkout_button)
        print("✅ Clicked 'CHECK OUT' button.")
    except TimeoutException:
        print("❌ 'CHECK OUT' button not found.")
# ---------------------------

# ---- CHECKOUT FUNCTIONS ----
def click_checkout_as_guest(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)

    try:
        # Wait for the "CHECKOUT AS GUEST" span to appear and be clickable
        guest_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='CHECKOUT AS GUEST']"
        )))
        guest_button.click()
        print("Clicked: CHECKOUT AS GUEST")
        time.sleep(2)  # Wait for next step to load

    except Exception as e:
        print(f"Error during guest checkout: {e}")
# ---------------------------

# delay = random.uniform(1.5, 4.0)
# print(f"Pausing for {delay:.2f} seconds before navigating...")
# time.sleep(delay)

# ---------------------------

# ---- EMAIL CONFIRMATION FUNCTIONS ----
def enter_email_and_confirm(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)
    email = "Tjoe@gmail.com"

    try:
        # Step 1: Enter email
        email_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@placeholder='Enter your email']"
        )))
        email_input.clear()
        email_input.send_keys(email)
        print(f"Entered email: {email}")
        time.sleep(1)

        # Step 2: Click the first "CONFIRM" button
        confirm_btn1 = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[contains(@class,'index_applyBtn__') and text()='CONFIRM']"
        )))
        confirm_btn1.click()
        print("Clicked first CONFIRM button")
        time.sleep(2)

        # Step 3: Click the second "CONFIRM" button
        # Wait for both buttons to be present
        WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((
            By.XPATH, "//button[.//span[text()='CONFIRM']]"
        )))
        
        confirm_btn2 = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[text()='CONFIRM']]"
        )))
        confirm_btn2.click()
        print("Clicked second CONFIRM button")
        time.sleep(2)
   
    except Exception as e:
        print(f"Error during email confirmation: {e}")
# ---------------------------


# ---- ADDRESS FUNCTIONS ----
def click_add_new_address(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)
    try:
        # Use XPath with exact text match
        add_address_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[normalize-space(text())='Add a new address']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", add_address_btn)
        add_address_btn.click()
        print("✅ Clicked: Add a new address")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Error clicking Add a new address: {e}")

# ---------------------------

# ---- MANUAL ADDRESS ENTRY FUNCTIONS ----
def click_enter_address_manually(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        manual_entry_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='Enter it manually' and contains(@class, 'addOrUpdateAddress_text__')]"
        )))
        manual_entry_btn.click()
        print("Clicked: Enter it manually")
        time.sleep(1.5)
    except Exception as e:
        print(f"Error clicking 'Enter it manually': {e}")
# ---------------------------

# ---- ADDRESS FORM FILLING FUNCTIONS ----
def fill_address_form(driver, timeout=15):
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
        print("Clicked Province dropdown")
        time.sleep(1)

        california_option = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[@class='ant-select-item-option-content' and text()='California']"
        )))
        california_option.click()
        print("Selected: California")
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
        print("Clicked: Save address")

        time.sleep(2)

    except Exception as e:
        print(f"Error while filling address form: {e}")
# ---------------------------

def click_again(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)

    # Step 1: Click "Edit" button
    try:
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='Edit' and contains(@class,'index_editBtn__')]"
        )))
        edit_btn.click()
        print("Clicked: Edit button")
    except Exception as e:
        print(f"Error clicking Edit button: {e}")
        return

    # Step 2: Click first "CONFIRM" button with class
    try:
        confirm_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//span[text()='CONFIRM' and contains(@class,'index_applyBtn__')]"
        )))
        confirm_btn.click()
        print("Clicked: First CONFIRM button")
    except Exception as e:
        print(f"Error clicking first CONFIRM button: {e}")
        return

    # Step 3: Click second "CONFIRM" button (generic)
    try:
        confirm_btn2 = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[.//span[normalize-space(text())='CONFIRM']]"
        )))
        confirm_btn2.click()
        print("Clicked: Second CONFIRM button")
    except Exception as e:
        print(f"Error clicking second CONFIRM button: {e}")


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
        send_email_noclick_pay("Checkout Failed", f"There was an error during checkout: {e}")

# ---------------------------

#---- PAYMENT FUNCTIONS ----
def fill_credit_card_and_pay(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)
    try:
        # 1. Click credit card radio button
        credit_card_option = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class, 'index_payIcon__') and .//img[contains(@src, 'credit_card')]]"
        )))
        driver.execute_script("arguments[0].click();", credit_card_option)  # JS click for reliability
        print("✅ Selected: Credit Card Option")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "iframe[name*='encryptedCardNumber'], iframe.js-iframe")
        ))
        time.sleep(3)
        
        # 2. Enter credit card info (inside iframes)

        # Wait for all Adyen iframes to load
        iframes = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CSS_SELECTOR, "iframe.js-iframe")
        )

        # ⚠️ Confirm we have all 3 required fields
        if len(iframes) < 3:
            raise Exception("Less than 3 Adyen iframes found")

        # === CARD NUMBER ===
        driver.switch_to.frame(iframes[0])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedCardNumber']"
        ))).send_keys("1234567812362542")
        driver.switch_to.default_content()

        # === EXPIRY DATE ===
        driver.switch_to.frame(iframes[1])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedExpiryDate']"
        ))).send_keys("01/29")
        driver.switch_to.default_content()

        # === CVC ===
        driver.switch_to.frame(iframes[2])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[data-fieldtype='encryptedSecurityCode']"
        ))).send_keys("222")
        driver.switch_to.default_content()

        # === NAME ON CARD ===
        # === NAME ON CARD ===
        name_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.NAME, "holderName"))
        )
        name_input.clear()
        name_input.send_keys("Try Im")
        # print("Entered: Name on Card")


        # 4. Capture total amount from Pay button
        pay_btn = wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[contains(@class, 'adyen-checkout__button--pay')]"
        )))
        total_text = pay_btn.text  # Example: "Pay $26.79"
        # print(f"Captured Total: {total_text}")

        # 5. Click the Pay button
        pay_btn.click()
        # print("Clicked: Pay button")

        # ✅ Send success email with total
        # send_email_payment_ok("💳 Payment Successful", f"Payment submitted successfully.\n\nAmount: {total_text}")

    except Exception as e:
        print(f"❌ Error during payment: {e}")
        # send_email_payment_notok("❌ Payment Failed", f"There was an error during payment:\n\n{e}")
# ---------------------------


def check_product():
    print("🚀 Launching browser...")

    driver = None
  
try:

    options = Options()
    options = uc.ChromeOptions()
    options.add_argument("--start-standalone")  # 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Launch Chrome
    driver = uc.Chrome(version_main=124, options=options)

    # options = webdriver.ChromeOptions()
    
    service = Service(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    


    driver.get(URL)
    
    add_to_bag_button = WebDriverWait(driver, WAIT_TIMEOUT).until(
    EC.presence_of_element_located((By.XPATH, BUTTON_XPATH))
    )

    print("✅ 'ADD TO BAG' button is available.")
    
    # Click the button if needed
    driver.execute_script("arguments[0].click();", add_to_bag_button)

    # Send email for availability
    send_email_avail()

    print("📧 Email for availability sent. Continuing with script...")

    # Proceed with the rest of your steps here

except TimeoutException:
    print("❌ 'ADD TO BAG' button not found. Stopping script.")
    
    # Optionally send a different email if it's not found
    send_email_unavail()
    
try:        

        accept_cookies_if_present(driver)
        automate_selections(driver)
        click_shopping_bag_icon(driver)
        time.sleep(2)
        click_custom_checkbox(driver)
        time.sleep(2)
        quick_scroll(driver)
        time.sleep(2)
        checkout(driver)
        time.sleep(2)
        click_checkout_as_guest(driver, timeout=15)
        time.sleep(2)
        enter_email_and_confirm(driver)
        time.sleep(2)
        click_add_new_address(driver)
        time.sleep(2)
        click_enter_address_manually(driver)
        time.sleep(2)
        fill_address_form(driver)
        time.sleep(5)
        click_again(driver)
        time.sleep(2)
        click_proceed_to_pay(driver)
        time.sleep(2)
        fill_credit_card_and_pay(driver)
        time.sleep(2)

        print("✅ Script finished automation steps.")
        print("🧪 Keeping browser open for observation...")
        time.sleep(60)  # Adjust or remove as needed       
  
        print("✅ Finished checking product availability.")
        print("🧪 About to screenshot before checking product")       

        # if  click_proceed_to_pay(driver):
        #     #fill_credit_card_and_pay(driver)
        #     time.sleep(2)   
        #     # checkout_as_member(driver)
        #     time.sleep(2)
        #     # enter_email_and_continue(driver)
        #     time.sleep(2)
        #     # enter_password_and_continue(driver)
        #     time.sleep(2)
        #     # select_default_address(driver)      
    
finally:
        print("🧹 Closing browser...")
        driver.quit()
            
if __name__ == "__main__":
    check_product()
