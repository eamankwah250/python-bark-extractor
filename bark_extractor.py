from multiprocessing.connection import wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def wait_until(xpath):
    WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))


# ****change chrome driver to your current chrome version**********
browser = webdriver.Chrome('./chromedriver.exe')
url = 'https://www.bark.com/en/us/login/'
browser.get(url)

# Login
email = browser.find_element(
    By.ID, "email").send_keys('barkleads@epibuild.com')
password = browser.find_element(By.ID, "password").send_keys('Thanku2Rob')
login = browser.find_element(By.XPATH, '//button[text() = "Log in"]').click()

# Click Leads
wait_until('//a[text() = "Leads"]')
leadsButton = browser.find_element(By.XPATH, '//a[text() = "Leads"]').click()

try:
    notification_text = '//u[text() = "{}"]'.format(
        "I don't want web notifications")
    wait_until(notification_text)
    notification = browser.find_element(By.XPATH, notification_text).click()
except:
    print('error occurs')


# TODO
# Iterate all clients
lead = browser.find_element(
    By.XPATH, '//div[@class="project-details-project-container"]')
image = browser.find_element(
    By.XPATH, '//img[@class="img-fluid rounded"]')
print(lead.text)
print(image.get_attribute('src'))
