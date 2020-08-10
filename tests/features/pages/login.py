from selenium.webdriver.common.by import By

from .base_page_object import *


class LoginPage(BasePage):

    def __init__(self, context):
        BasePage.__init__(
            self,
            context.browser,
            base_url=get_from_config('url'))

    locator_dictionary = {
        'username_input': (By.XPATH, '//input[@name="username"]'),
        'password_input': (By.XPATH, '//input[@name="password"]'),
        'login_button': (By.ID, 'login_btn'),
        'logged_user': (By.XPATH, '//li/span[contains(text(), "Witaj")]'),
    }

    def enter_username(self, username):
        self.username_input.send_keys(username)

    def enter_password(self, password):
        self.password_input.send_keys(password)

    def click_login_button(self):
        self.login_button.click()

    def get_user_logged_in(self):
        return self.logged_user.text.strip('Witaj,')
