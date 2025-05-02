# Author: Trey Songz
# Date: 2024-01-01  
# Description: This script automates the process of checking the availability of a product on the POP MART website. 
# It sends email notifications based on its availability. 
# It uses Selenium for web automation and smtplib for sending emails.
# ------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import smtplib
import sys   # For exit codes
import time  # For sleep
import undetected_chromedriver as uc
from email.message import EmailMessage
print(sys.version)

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
def send_email():
    msg = EmailMessage()

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Email for availability sent.")
    except Exception as e:
        print(f"Error sending email: {e}")

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
# print("✅ Accepting cookies if present")
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
            driver.save_screenshot("before_add_to_bag.png")
            btn_xpath = "//div[text()='ADD TO BAG']"
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, btn_xpath)))
            btn.click()
            print("✅ Item added to bag.")
            time.sleep(3)
            driver.save_screenshot("after_add_to_bag.png")
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
    driver.save_screenshot("Done_with_auto_select.png")


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
        driver.save_screenshot("shopping_bag_click_error.png")
        raise
#   ---------------------------

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

# ---- EMAIL CONFIRMATION FUNCTIONS ----
def enter_email_and_confirm(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)
    email = "try.shai.im@gmail.com"

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
        add_address_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//div[text()='Add a new address' and contains(@class,'index_addAddressBtn__')]"
        )))
        add_address_btn.click()
        print("Clicked: Add a new address")
        time.sleep(2)  # Wait for form to appear
    except Exception as e:
        print(f"Error clicking Add a new address: {e}")
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
        zip_code.send_keys("92683")

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

# ---- PROCEED TO PAY FUNCTIONS ----
def click_proceed_to_pay(driver, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        proceed_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class, 'index_placeOrderBtn__') and text()='PROCEED TO PAY']"
        )))
        proceed_btn.click()
        print("Clicked: PROCEED TO PAY")
        time.sleep(2)

            # ✅ Success email
        send_email("Checkout Successful", "The checkout proceeded successfully.")

    except Exception as e:
        print(f"Error clicking PROCEED TO PAY: {e}")

        # ❌ Failure email
        send_email("Checkout Failed", f"There was an error during checkout: {e}")
# ---------------------------

# ---- PAYMENT FUNCTIONS ----
# def fill_credit_card_and_pay(driver, timeout=15):
#     wait = WebDriverWait(driver, timeout)
#     try:
#         # 1. Click credit card radio button
#         credit_card_radio = wait.until(EC.element_to_be_clickable((
#             By.XPATH, "//span[contains(@class, 'index_radio__')]"
#         )))
#         credit_card_radio.click()
#         print("Selected: Credit Card Option")
#         time.sleep(1)

#         # 2. Enter credit card info (inside iframes)

#         # Card Number
#         driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[name*='encryptedCardNumber']"))
#         wait.until(EC.presence_of_element_located((
#             By.CSS_SELECTOR, "input[data-fieldtype='encryptedCardNumber']"
#         ))).send_keys("5178059636804644")
#         driver.switch_to.default_content()

#         # Expiry Date
#         driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[name*='encryptedExpiryDate']"))
#         wait.until(EC.presence_of_element_located((
#             By.CSS_SELECTOR, "input[data-fieldtype='encryptedExpiryDate']"
#         ))).send_keys("01/29")
#         driver.switch_to.default_content()

#         # Security Code
#         driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[name*='encryptedSecurityCode']"))
#         wait.until(EC.presence_of_element_located((
#             By.CSS_SELECTOR, "input[data-fieldtype='encryptedSecurityCode']"
#         ))).send_keys("291")
#         driver.switch_to.default_content()

#         # 3. Name on card
#         name_input = wait.until(EC.presence_of_element_located((
#             By.ID, "adyen-checkout-holderName-1746116986608"
#         )))
#         name_input.clear()
#         name_input.send_keys("Try Im")

#         # 4. Capture total amount from Pay button
#         pay_btn = wait.until(EC.presence_of_element_located((
#             By.XPATH, "//button[contains(@class, 'adyen-checkout__button--pay')]"
#         )))
#         total_text = pay_btn.text  # Example: "Pay $26.79"
#         print(f"Captured Total: {total_text}")

#         # 5. Click the Pay button
#         pay_btn.click()
#         print("Clicked: Pay button")

#         # ✅ Send success email with total
#         send_email("💳 Payment Successful", f"Payment submitted successfully.\n\nAmount: {total_text}")

#     except Exception as e:
#         print(f"❌ Error during payment: {e}")
#         send_email("❌ Payment Failed", f"There was an error during payment:\n\n{e}")
# # ---------------------------



# def checkout_as_member(driver):
#     try:
#         member_checkout_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//span[text()="CHECKOUT AS MEMBER"]/ancestor::button'))
#         )
#         driver.execute_script("arguments[0].click();", member_checkout_button)
#         print("✅ Clicked 'CHECKOUT AS MEMBER' button.")
#     except TimeoutException:
#         print("❌ 'CHECKOUT AS MEMBER' button not found.")

# def enter_email_and_continue(driver):
#     try:
#         email_input = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "email"))
#         )
#         email_input.clear()
#         email_input.send_keys("try@cogosystems.com")
#         print("✅ Entered email.")

#         continue_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "index_loginButton__nvmup"))
#         )
#         continue_button.click()
#         print("✅ Clicked CONTINUE after email.")
#     except TimeoutException:
#         print("❌ Email field or CONTINUE button not found.")

# def enter_password_and_continue(driver):
#     try:
#         # Step 1: Enter the password
#         password_input = WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.ID, "password"))
# )
#         password_input.clear()
#         password_input.send_keys("Sh@isters7124")
#         print("✅ Entered password.")

#         # Step 2: Click the SIGN IN button
#         sign_in_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((
#                 By.XPATH, '//button[@type="submit" and contains(@class, "index_loginButton__nvmup") and text()="SIGN IN"]'
#             ))
#         )
#         # continue_button.click()
#         print("✅ Clicked 'SIGN IN' after password.")
#     except TimeoutException:
#         print("❌ Password field or 'SIGN IN' button not found.")
#         time.sleep(20)

# def select_default_address(driver):
#     try:
#         default_address = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "addressItem_addressContentActive__0uIAd") and .//div[contains(@class, "addressItem_defaultBtn__T2uJM") and contains(text(), "Default")]]'))
#         )
#         driver.execute_script("arguments[0].scrollIntoView(true);", default_address)
#         driver.execute_script("arguments[0].click();", default_address)
#         print("✅ Selected the default address.")
#     except TimeoutException:
#         print("❌ Default address block not found or not clickable.")

# # def click_proceed_to_pay(driver):
#     try:
#         proceed_btn = WebDriverWait(driver, 15).until(
#             EC.element_to_be_clickable((
#                 By.XPATH,
#                 '//button[contains(@class, "index_placeOrderBtn__wgYr6") and text()="PROCEED TO PAY"]'
#             ))
#         )
#         driver.execute_script("arguments[0].scrollIntoView(true);", proceed_btn)
#         driver.execute_script("arguments[0].click();", proceed_btn)
#         print("✅ Clicked 'PROCEED TO PAY'.")
#     except TimeoutException:
#         print("❌ 'PROCEED TO PAY' button not found or not clickable.")

# # def select_credit_card_option(driver):
#     try:
#         credit_card_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, "index_radioActive__K2Sdi"))
#         )
#         credit_card_button.click()
#         print("Selected credit card option.")
#     except TimeoutException:
#         print("Credit card option not found.")

def check_product():
    print("🚀 Launching browser...")

    driver = None
  

try:

        

    # options = uc.ChromeOptions()
    # options.add_argument("--start-maximized")

    # driver = uc.Chrome(options=options)

    # # options.add_argument("--headless")  # Uncomment if you want headless
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36")

    # driver = uc.Chrome(options=options)

    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
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
        click_custom_checkbox(driver)
        checkout(driver)
        click_checkout_as_guest(driver, timeout=15)
        enter_email_and_confirm(driver)
        time.sleep(2)
        click_add_new_address(driver)
        time.sleep(2)
        click_enter_address_manually(driver)
        time.sleep(2)
        fill_address_form(driver)
        time.sleep(2)
        click_proceed_to_pay(driver)

        print("✅ Script finished automation steps.")
        print("🧪 Keeping browser open for observation...")
        time.sleep(60)  # Adjust or remove as needed
        
    #     WebDriverWait(driver, WAIT_TIMEOUT).until(
    #         EC.presence_of_element_located((By.XPATH, BUTTON_XPATH))
    #     )
    #     print("✅ 'ADD TO BAG' button is available.")
    #     send_email_avail()

    # except TimeoutException:

    #     print("❌ 'ADD TO BAG button is NOT available.")
    #     send_email_unavail()

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     send_email_unavail()
   
        print("✅ Finished checking product availability.")
        print("🧪 About to screenshot before checking product")
        driver.save_screenshot("before_checking_product.png")

        if  click_proceed_to_pay(driver):
            #fill_credit_card_and_pay(driver)
            time.sleep(2)   
            # checkout_as_member(driver)
            time.sleep(2)
            # enter_email_and_continue(driver)
            time.sleep(2)
            # enter_password_and_continue(driver)
            time.sleep(2)
            # select_default_address(driver)
    
    
    # except Exception as e:
    #     print(f"❌ An error occurred during automation: {e}")
    
finally:
        print("🧹 Closing browser...")
        driver.quit()
            
if __name__ == "__main__":
    check_product()
