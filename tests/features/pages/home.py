from selenium.webdriver.common.by import By
from .base_page_object import *


class HomePage(BasePage):

    def __init__(self, context):
        BasePage.__init__(
            self,
            context.browser,
            base_url=get_url_from_config())

    locator_dictionary = {
        "login_button": (By.XPATH, "//a[@name='login_href']"),
        "logged_user": (By.XPATH, "//li/span[contains(text(), 'Witaj')]"),
    }

    def open_login_page(self):
        try:
            self.login_button.click()
        except:
            print('User is already logged in as: ' + self.logged_user.text.strip('Witaj, '))
