import os
import wget
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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
username.send_keys("type-email")
password.clear()
password.send_keys("type-password")

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

for restaurant in restaurants:
    restaurant_url = restaurant.get_attribute("href")
    driver.execute_script("window.open(arguments[0])", restaurant_url)
    driver.switch_to.window(driver.window_handles[1])

    try:
        element = driver.find_element(
            By.XPATH,
            "//h4[contains(@class, 'css-e29med') and contains (text(), 'Make a Reservation')]",
        )
        print(element.text)

    except NoSuchElementException:
        print("Not here")
        driver.close()
        driver.switch_to.window(original_window)
