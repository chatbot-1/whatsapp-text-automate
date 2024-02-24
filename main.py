from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager

# Config
login_time = 30                 # Time for login (in seconds)
new_msg_time = 5                # Time for a new message (in seconds)
send_msg_time = 5               # Time for sending a message (in seconds)
country_code = 91               # Set your country code
action_time = 2                 # Set time for button click action
image_path = 'C:/Users/HP/Pictures/Screenshots/omg.png'        # Absolute path to you image
invalid_phone_popup_selector = 'number does not exist on the whatsapp'  # Update this selector based on the actual popup

# Create driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Encode Message Text
with open('message.txt', 'r') as file:
    msg = file.read()

# Open browser with default link
link = 'https://web.whatsapp.com'
driver.get(link)
time.sleep(login_time)

# Loop Through Numbers List
with open('numbers.txt', 'r') as file:
    for n in file.readlines():
        num = n.rstrip()
        link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
        driver.get(link)
        time.sleep(new_msg_time)

        try:
            # Check if invalid phone number popup appears
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, invalid_phone_popup_selector)))
            print(f"Invalid number detected: {num}, skipping...")
            pass  # Skip this number and proceed with the next
        except TimeoutException:
            # Proceed if no popup detected
            pass

        # Click on button to load the input DOM
        if image_path:
            try:
                attach_btn = driver.find_element(By.CSS_SELECTOR, '._1OT67')
                attach_btn.click()
                time.sleep(action_time)
                # Find and send image path to input
                msg_input = driver.find_elements(By.CSS_SELECTOR, '._2UNQo input')[1]
                msg_input.send_keys(image_path)
                time.sleep(action_time)
            except NoSuchElementException:
                print("Failed to find the attachment button or input field. Interface might have changed.")
                continue

        # Start the action chain to write the message
        actions = ActionChains(driver)
        for line in msg.split('\n'):
            actions.send_keys(line)
            # SHIFT + ENTER to create next line
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(send_msg_time)

# Quit the driver
driver.quit()
