from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from Database import Database
from Client import Client
from PSTtime import pst_date


# wait 30 seconds for the element with xpath to be found
def wait_until(xpath):
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except:
        print('error occurs')


# headless chrome
# comment it out to see the actual flow.
options = Options()
# options.headless = True
# options.add_argument('window-size=1920x1080')

# ****change chrome driver to your current chrome version**********
browser = webdriver.Chrome('./chromedriver.exe', options=options)
url = 'https://www.bark.com/en/us/login/'
browser.get(url)

# Login
wait_until('//*[@id="email"]')
email = browser.find_element(
    By.ID, "email").send_keys('barkleads@epibuild.com')
password = browser.find_element(By.ID, "password").send_keys('Thanku2Rob')
login = browser.find_element(By.XPATH, '//button[text() = "Log in"]').click()

# Click Leads
wait_until('//a[text() = "Leads"]')
leadsButton = browser.find_element(By.XPATH, '//a[text() = "Leads"]').click()

# Click Notification alert
try:
    notification_text = '//u[text() = "{}"]'.format(
        "I don't want web notifications")
    wait_until(notification_text)
    notification = browser.find_element(By.XPATH, notification_text).click()
except:
    print('error occurs')

container = browser.find_element(By.XPATH, '//div[@class="items"]')
leads = container.find_elements(
    By.XPATH, '//*[@id="dashboard-projects"]/div[6]/div')

# Client class list
Clients = []

# Iterate all client
for lead in leads:
    lead.click()
    leadData = browser.find_element(
        By.XPATH, '//div[@class="project-details-project-container"]')
    mapImage = browser.find_element(
        By.XPATH, '//img[@class="img-fluid rounded"]')
    data = leadData.text
    first_name = data[0]
    data_received = data[1]
    job_type = data[2]
    print(data)
    print(mapImage.get_attribute('src'))
    print('-' * 100)
    time.sleep(1)

# Load more
loadMoreBtn = browser.find_element(
    By.XPATH, '//button[text() = "Load more"]').click()
time.sleep(6)


# Database connection
# if __name__ == '__main__':
#     db = Database(db="Team2DB", user="Team2", password="Team2",
#                   port="5432", host="138.26.48.83")
#     db.connect()
#     db.close()
