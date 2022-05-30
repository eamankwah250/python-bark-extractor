from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
from Database import Database
from PSTtime import pst_date


# wait 30 seconds for the element with xpath to be found
def wait_until(xpath):
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except:
        print('error occurs')


def check_urgency(browser, xpath):
    try:
        browser.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return "Urgent - wants to be contacted ASAP"
    return "Not Urgent"


def check_attachments(browser, xpath):
    try:
        attachments = browser.find_elements(By.XPATH, xpath)
        list = []
        for attachment in attachments:
            list.append(attachment.get_attribute('href'))
    except NoSuchElementException:
        return "No Attachment"
    return list


# ****change chrome driver to your current chrome version**********
browser = webdriver.Chrome('./chromedriver.exe')
browser.maximize_window()
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

# Load more Button
# One click = 15 more leads
# change numOfclickBtn var to control the number of reads to retrieve.
numOfclickBtn = 5
for i in range(numOfclickBtn):
    loadMoreBtn = browser.find_element(
        By.XPATH, '//button[text() = "Load more"]').click()
    time.sleep(1)
    wait_until('//button[text() = "Load more"]')

leads = browser.find_elements(
    By.XPATH, '//*[@id="dashboard-projects"]/div[6]/div')

numOfLeads = len(leads)
print(numOfLeads)  # number of leads
# Iterate all client
for i in range(numOfLeads):
    element = leads[i]
    ActionChains(browser).move_to_element(
        element).click(element).perform()
    print(i)
    topData = browser.find_element(
        By.XPATH, '//div[@class="project-top"]').text.splitlines()
    first_name = topData[0]
    data_received = topData[1]
    ago = re.findall(r'(\d+)(\w)', data_received)
    if ago[0][1] == 's':
        date = pst_date(0, 0, 0, int(ago[0][0]))
    elif ago[0][1] == 'm':
        date = pst_date(0, 0, int(ago[0][0]), 0)
    elif ago[0][1] == 'h':
        date = pst_date(0, int(ago[0][0]), 0, 0)
    else:
        date = pst_date(int(ago[0][0]), 0, 0, 0)
    job_type = topData[2]
    state = topData[3]
    online = browser.find_element(
        By.XPATH, '//span[@class="location-notes"]').text
    online = online if online != '' else 'Local Work Only'
    phone = browser.find_element(
        By.XPATH, '//span[@class="buyer-telephone-display d-flex"]').text
    isVerified = browser.find_element(
        By.XPATH, '//div[@class="verified-phone-container ml-3"]').text
    if isVerified != '':
        phone += " Verified"
    email = browser.find_element(
        By.XPATH, '//span[@class="buyer-email-display text-break"]').text
    responses = browser.find_element(
        By.XPATH, '//span[@class="response-cap-and-count-text"]').text
    urgent = check_urgency(
        browser, '//div[@class="project-details-urgent d-none"]')
    credits = browser.find_element(
        By.XPATH, '//span[@class="num-credits-resp pl-2 text-grey-400"]').text
    details = browser.find_element(
        By.XPATH, '//*[@id="dashboard-project-details"]/div[3]/div[2]').text  # .splitlines()
    attachment = check_attachments(
        browser, '//a[@title="Click to see this image in a new window"]')
    mapImage = browser.find_element(
        By.XPATH, '//img[@class="img-fluid rounded"]').get_attribute('src')

    print('firstname: {}'.format(first_name))
    print('data_received: {}'.format(date))
    print('job_type: {}'.format(job_type))
    print('state: {}'.format(state))
    print('phone: {}'.format(phone))
    print('email: {}'.format(email))
    print('responses: {}'.format(responses))
    print('urgent: {}'.format(urgent))
    print('credits: {}'.format(credits))
    print('details: {}'.format(details))
    print('attachment: {}'.format(attachment))
    print('mapImage: {}'.format(mapImage))
    print('-' * 60)
    time.sleep(1)


# Database connection
# if __name__ == '__main__':
#     db = Database(db="Team2DB", user="Team2", password="Team2",
#                   port="5432", host="138.26.48.83")
#     db.connect()
#     db.close()
