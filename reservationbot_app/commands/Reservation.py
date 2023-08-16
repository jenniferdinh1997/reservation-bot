import os
import wget
import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .constants import ROOT_URL

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# defining the browser
driver = webdriver.Chrome(options=chrome_options)

# logging in
def authenticate(driver):
    driver.get(ROOT_URL)

    login_form = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ajax-login"))
    )

    username = login_form.find_element(By.NAME, "email")
    password = login_form.find_element(By.NAME, "password")

    username.clear()
    username.send_keys("example@gmail.com")
    password.clear()
    password.send_keys("example password")

    # login_button = (
    #     WebDriverWait(driver, 2)
    #     .until(
    #         EC.element_to_be_clickable(
    #             (By.CSS_SELECTOR, "button.ybtn.ybtn--primary.ybtn--big.submit.ybtn-full")
    #         )
    #     )
    #     .click()
    # )
    driver.find_element(By.CSS_SELECTOR, "button.ybtn.ybtn--primary.ybtn--big.submit.ybtn-full").click()
    return driver

# go to user's collections
collections_link = (
    WebDriverWait(driver, 8)
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

# making a yelp reservation for each page
reservation_data = []
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
                try:
                    button = slot.find_element(By.TAG_NAME, "button")
                    if not button.get_attribute("disabled"):
                        button.click()
                        break
                except NoSuchElementException:
                    print("no slot")
                    continue
            
            confirm_reservation = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(@type, 'submit') and contains (@class, 'css-12anb14')]"
                        )
                    )
            )
            confirm_reservation.click()

            # reserved_name = wait.until(
            #     EC.presence_of_element_located(
            #         (
            #             By.XPATH,
            #             "//a[contains(@role, 'link') and contains (@class, 'businessTitleLink__09f24__yn6_N')]"
            #         )
            #     )
            # )
            # reserved_time = wait.until(
            #     EC.presence_of_element_located(
            #         (
            #             By.XPATH,
            #             "//span[contains(@class, 'reservationInfoText__09f24__K6yrO')]"
            #         )
            #     )
            # )

            # print(reservation_data, "data")

            # print(reserved_name.text, "name", reserved_time.text(), "time")

            driver.close()
            driver.switch_to.window(original_window)

            # reservation_data.append({
            #     "Name": reserved_name.text,
            #     "Time": reserved_time.text
            # })

        except TimeoutException:
            print("Not here")
            driver.close()
            driver.switch_to.window(original_window)

    except StaleElementReferenceException:
        print("Stale element")
        continue

# for entry in reservation_data:
#     print(entry["Name"], "name", entry["Time"], "time")