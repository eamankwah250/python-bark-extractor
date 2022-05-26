# pip install openpyxl selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# change chrome driver to your current chrome version
browser = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.bark.com'
browser.get(url)
# signin = browser.find_element(By.XPATH, '//a[text() = "Try for free "]')
# signin.click()
