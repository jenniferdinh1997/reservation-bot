import os
import wget
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# defining the browser
driver = webdriver.Chrome(options=chrome_options)

# opening the webpage
driver.get("https://www.yelp.com/login")

# logging in
login_form = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ajax-login"))
)

username = login_form.find_element(By.NAME, "email")
password = login_form.find_element(By.NAME, "password")

username.clear()
username.send_keys("email")
password.clear()
password.send_keys("password")

login_button = (
    WebDriverWait(driver, 2)
    .until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.ybtn.ybtn--primary.ybtn--big.submit.ybtn-full")
        )
    )
    .click()
)

# go to user's collections
collections_link = (
    WebDriverWait(driver, 5)
    .until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collections']")))
    .click()
)

user_collections = (
    WebDriverWait(driver, 5)
    .until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/collections/user']")))
    .click()
)

# select reservation collection
chosen_phrase = "OC/LA"
reservation_collection = (
    WebDriverWait(driver, 10)
    .until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//h4[contains(@class, 'u-space-t2') and contains (text(), '{chosen_phrase}')]",
            )
        )
    )
    .click()
)

# clicking on each page in collection to see if able to make yelp reservation
restaurants = driver.find_elements(By.CLASS_NAME, "biz-name")
original_window = driver.current_window_handle
wait = WebDriverWait(driver, 7)

for restaurant in restaurants:
    try:
        restaurant_url = restaurant.get_attribute("href")
        driver.execute_script("window.open(arguments[0])", restaurant_url)
        driver.switch_to.window(driver.window_handles[1])

        try:
            element = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//h4[contains(@class, 'css-e29med') and contains (text(), 'Make a reservation')]",
                    )
                )
            )

            reservation_link = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "css-1drn1lx"))
            )
            reservation_link.click()

            time_slots = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "availability-slot")
                )
            )
            for slot in time_slots:
                print("slot:", slot.text)
                button = slot.find_element(By.TAG_NAME, "button")
                print("button", button.text)
                if button.text == "7:00 pm":
                    button.click()
                else:
                    continue
            
            confirm_reservation = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//span[contains(@class, css-1enow5j') and contains (text(), 'Confirm')]"
                        )
                    )
            )
            confirm_reservation.click()

        except TimeoutException:
            print("Not here")
            driver.close()
            driver.switch_to.window(original_window)

    except StaleElementReferenceException:
        print("Stale element")
        continue
