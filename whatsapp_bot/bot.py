import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("--user-data-dir=/tmp/User_Data")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.get("https://web.whatsapp.com")
wait = WebDriverWait(driver, 60)
# print("Please Scan the QR Code and press enter")
contact = "_"
inp_xpath_search = "//input[@title='Search or start new chat']"
input_box_search = wait.until(
    lambda driver: driver.find_element(By.XPATH, inp_xpath_search)
)
input_box_search.click()
time.sleep(2)
input_box_search.send_keys(contact)
time.sleep(2)

# input()
driver.quit()
