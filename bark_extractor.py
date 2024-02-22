from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import re
import time
from Database import Database
from PSTtime import pst_date


# wait 30 seconds for the element with xpath to be found
def wait_until(browser, xpath):
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except:
        print('error occurs')


def check_urgency(browser, xpath):
    try:
        browser.find_element(By.XPATH, xpath)
        return "Not Urgent"
    except NoSuchElementException:
        return "Urgent - wants to be contacted ASAP"


def check_remote_option(browser, xpath):
    try:
        browser.find_element(By.XPATH, xpath)
        return "Non Remote Lead"
    except NoSuchElementException:
        return "Happy to receive service online or remotely"


def check_attachments(browser, xpath):
    try:
        attachments = browser.find_elements(By.XPATH, xpath)
        list = []
        for attachment in attachments:
            list.append(attachment.get_attribute('href'))
        return list
    except NoSuchElementException:
        return list


# Click Notification alert
def click_notification(browser):
    try:
        notification_text = '//u[text() = "{}"]'.format(
            "I don't want web notifications")
        wait_until(browser, notification_text)
        browser.find_element(By.XPATH, notification_text).click()
    except:
        print('error occurs')


# ****change chrome driver to your current chrome version**********
# Main function
def mainFn():
    browser = webdriver.Chrome(service= Service('./chromedriver.exe'))
    browser.maximize_window()
    url = 'https://www.bark.com/en/us/login/'
    browser.get(url)

    # Login
    wait_until(browser, '//*[@id="email"]')
    email = browser.find_element(
        By.ID, "email").send_keys('barkleads@epibuild.com')
    browser.find_element(By.ID, "password").send_keys('Thanku2Rob')
    browser.find_element(By.XPATH, '//button[text() = "Log in"]').click()

    click_notification(browser)

    # Click Leads
    wait_until(browser, '//a[text() = "Leads"]')
    browser.find_element(By.XPATH, '//a[text() = "Leads"]').click()

    # Load more Button
    # One click = 15 more leads
    # change numOfclickBtn var to control the number of reads to retrieve.
    numOfclickBtn = 7
    for i in range(numOfclickBtn):
        wait_until(browser, '//button[text() = "Load more"]')
        loadMoreBtn = browser.find_element(
            By.XPATH, '//button[text() = "Load more"]')
        time.sleep(1)
        ActionChains(browser).scroll_to_element(
            loadMoreBtn).click(loadMoreBtn).perform()
        time.sleep(2)

    # Iterate all lead
    leads = browser.find_elements(
        By.XPATH, '//*[@id="dashboard-projects"]/div[6]/div')
    for i in range(len(leads)):
        element = leads[i]
        ActionChains(browser).scroll_to_element(
            element).click(element).perform()
        time.sleep(1)
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
            browser, '//div[@class="project-details-urgent font-weight-regular text-grey-600 mb-2 mt-2 d-none"]')
        remote = check_remote_option(
            browser, '//div[@class="project-name-location project-name-location-notes d-none d-md-block hidden"]')
        credits = browser.find_element(
            By.XPATH, '//span[@class="tw-text-dark-blue-500"]').text
        details = browser.find_element(
            By.XPATH, '//*[@id="dashboard-project-details"]/div[3]/div[2]').text
        detail = details.splitlines()
        budget = "I'm not sure"
        for index in range(len(detail)):
            if "budget" in detail[index]:
                try:
                    budget = detail[index + 1]
                except IndexError:
                    budget = "I'm not sure"
        attachment = check_attachments(
            browser, '//a[@title="Click to see this image in a new window"]')
        mapImage = browser.find_element(
            By.XPATH, '//*[@id="dashboard-project-details"]/div[3]/div[2]/div[3]/div[2]/img').get_attribute('src')
        
        count= db.countQuery(first_name, state, job_type)
        #print(count)

        if(count < 1):
            db.insertQuery(first_name, date, job_type,
                       state, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote)
            print (first_name + " inserted")
        else:
            db.updateQuery(first_name, date, job_type, state, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote)
            print(first_name + " updated")
        




# Database connection
if __name__ == '__main__':
    db = Database(db="epibark", user="postgres", password="ThankU2Rob@bark",
                  port="5432", host="34.42.148.111")
    db.connect()
    mainFn()
    db.close()
