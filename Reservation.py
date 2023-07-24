import os
import wget
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# defining the browser
driver = webdriver.Chrome()

# opening the webpage
driver.get("https://www.yelp.com/")