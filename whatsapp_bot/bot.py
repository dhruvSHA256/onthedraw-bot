from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class WABot:
    def __init__(self) -> None:
        options = Options()
        options.add_argument("--user-data-dir=/tmp/User_Data")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("—-no-sandbox")
        # options.add_argument("-—headless")

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.driver.implicitly_wait(30)
        self.wait = WebDriverWait(self.driver, 30)

    def start(self) -> None:
        self.driver.get("https://web.whatsapp.com")
        # print("Please Scan the QR Code and press enter")
        # input()

    def get_contact(self, contact: str):
        contact_xpath = f"//span[@title='{contact}']"
        search_xpath = "//button[@aria-label='Search or start new chat']"

        self.wait.until(Ec.presence_of_element_located((By.XPATH, search_xpath)))
        input_box_search = self.driver.find_element(By.XPATH, search_xpath)
        input_box_search.click()
        input_box_search.send_keys(contact)

        self.wait.until(Ec.presence_of_element_located((By.XPATH, contact_xpath)))
        selected_contact = self.driver.find_element(By.XPATH, contact_xpath)
        return selected_contact

    def get_input_box(self):
        input_box_xpath = "//div[@title='Type a message']"
        self.wait.until(Ec.presence_of_element_located((By.XPATH, input_box_xpath)))
        return self.driver.find_element(By.XPATH, input_box_xpath)

    def get_attach_button(self):
        attach_xpath = "//span[@data-testid='clip']"
        self.wait.until(Ec.presence_of_element_located((By.XPATH, attach_xpath)))
        return self.driver.find_element(By.XPATH, attach_xpath)

    def get_send_attach_button(self):
        send_attach_xpath = "//span[@data-testid='send']"
        self.wait.until(Ec.presence_of_element_located((By.XPATH, send_attach_xpath)))
        return self.driver.find_element(By.XPATH, send_attach_xpath)

    def get_send_button(self):
        button_xpath = "//button[@aria-label='Send']"
        self.wait.until(Ec.presence_of_element_located((By.XPATH, button_xpath)))
        return self.driver.find_element(By.XPATH, button_xpath)

    def get_attach_box(self):
        attach_box_xpath = (
            "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
        )
        attach_box = self.driver.find_element(By.XPATH, attach_box_xpath)
        return attach_box

    def get_attach_picture_button(self):
        attach_photo_xpath = "//button[@aria-label='Photos & Videos']"
        self.wait.until(Ec.presence_of_element_located((By.XPATH, attach_photo_xpath)))
        attach_photo_button = self.driver.find_element(By.XPATH, attach_photo_xpath)
        return attach_photo_button

    def select_contact(self, name):
        # check if already selected contact
        # if span element present with the following attrs
        #   data-testid="conversation-info-header-chat-title"
        #   title=contact
        # then contact already selected no need to search again
        # try:
        #     self.driver.find_element(
        #         By.XPATH,
        #         f"//span[@data-testid='conversation-info-header-chat-title' and @title='{name}']",
        #     )
        # except:
        contact = self.get_contact(name)
        contact.click()

    def send_message(self, message):
        input_box = self.get_input_box()
        input_box.click()
        input_box.send_keys(message)
        send_button = self.get_send_button()
        send_button.click()

    def send_attachment(self, path):
        attach_button = self.get_attach_button()
        attach_button.click()
        attach_box = self.get_attach_box()
        attach_box.send_keys(path)
        send_attach_button = self.get_send_attach_button()
        send_attach_button.click()
