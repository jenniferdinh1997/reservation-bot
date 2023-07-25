import os
import wget
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# defining the browser
driver = webdriver.Chrome(options=chrome_options)

# opening the webpage
driver.get("https://www.yelp.com/login?return_url=https%3A%2F%2Fwww.yelp.com%2F")

# logging in
login_form = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ajax-login"))
)

username = login_form.find_element(By.NAME, "email")
password = login_form.find_element(By.NAME, "password")

username.clear()
username.send_keys("username")
password.clear()
password.send_keys("password")

button = (
    WebDriverWait(driver, 2)
    .until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.ybtn.ybtn--primary.ybtn--big.submit.ybtn-full")
        )
    )
    .click()
)
