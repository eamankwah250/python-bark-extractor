from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
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
    flag = True

    # Login
    while flag == True:
        wait_until(browser, '//*[@id="email"]')
        email = browser.find_element(
            By.ID, "email").send_keys('barkleads@epibuild.com')
        browser.find_element(By.ID, "password").send_keys('Thanku2Rob')
        browser.find_element(By.XPATH, '//button[text() = "Log in"]').click()
        time.sleep(2)
        currentPage= browser.current_url
        if currentPage != url:
            flag= False
            break
        time.sleep(5)
    
    click_notification(browser)

    # Click Leads
    wait_until(browser, '//a[text() = "Leads"]')
    browser.find_element(By.XPATH, '//a[text() = "Leads"]').click()

    # Load more Button
    # One click = 15 more leads
    # change numOfclickBtn var to control the number of reads to retrieve.
    numOfclickBtn = 7
    # When a new iteration begins, we want to start from where we left off
    endOfPrevIteration = 0
    for i in range(numOfclickBtn):
        print("I is:"+ str(i))
        wait_until(browser, '//button[text() = "Load more"]')
        loadMoreBtn = browser.find_element(
            By.XPATH, '//button[text() = "Load more"]')
        time.sleep(2)
        browser.execute_script("arguments[0].scrollIntoView",loadMoreBtn)
        time.sleep(2)

        # Iterate all lead
        leads = browser.find_elements(
            By.XPATH, '//*[@id="__rctLeadsList"]/div/div/div[1]//button')
        #print(len(leads))
        for j in range(endOfPrevIteration,len(leads)):
            element = leads[j]
            ActionChains(browser).scroll_to_element(
                element).click(element).perform()
            time.sleep(1)
            print(j)
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
                By.XPATH, '//*[@id="ghg-on-leads-details"]/div/div[1]/div/span').text
            details = browser.find_element(
                By.XPATH, '//*[@id="dashboard-project-details"]/div[3]/div/div[2]/div').text
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
                By.XPATH, '//*[@id="dashboard-project-details"]/div[3]/div/div[2]/div/div[2]/div[2]/img').get_attribute('src')
        
            

            count= db.countQuery(first_name, state, job_type)
            print(count)

            if(count < 1):
                db.insertQuery(first_name, date, job_type,
                           state, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote)
                print (first_name + " inserted")
            else:
                db.updateQuery(first_name, date, job_type, state, phone, email, responses, urgent, credits, details, budget, attachment, mapImage, remote)
                print(first_name + " updated")
        endOfPrevIteration = len(leads)
    
        
        




# Database connection
if __name__ == '__main__':
    db = Database(db="epifinde_EpiBark", user="epifinde_epibark", password="Thanku2Rob@bark",
                  port="5432", host="50.87.21.232")
   # db.connect()
    mainFn()
  #  db.close()
