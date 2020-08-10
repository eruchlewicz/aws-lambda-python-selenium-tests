from selenium.webdriver.common.by import By

from .base_page_object import *


class AccountPage(BasePage):

    def __init__(self, context):
        BasePage.__init__(
            self,
            context.browser,
            base_url=get_from_config('url'))

    locator_dictionary = {
        'account_header': (By.XPATH, '//h2[text()="Dane"]'),
        'change_password_header': (By.XPATH, '//h2[text()="Zmiana hasła"]'),
        'change_password_button': (By.XPATH, '//button[text()="Zmień hasło"]'),
        'data_frame': (By.CSS_SELECTOR, '.col-lg-10.mx-auto'),
        'current_password_input': (By.ID, 'id_old_password'),
        'new_password_input_1': (By.ID, 'id_new_password1'),
        'new_password_input_2': (By.ID, 'id_new_password2'),
    }

    def account_page_is_opened(self):
        try:
            return self.account_header.is_displayed()
        except:
            return False

    def user_data_is_displayed(self, text):
        try:
            return text in self.data_frame.text
        except:
            return False

    def change_password_button_is_displayed(self):
        try:
            return self.change_password_button.is_displayed()
        except:
            return False

    def change_password_page_is_opened(self):
        try:
            return self.change_password_header.is_displayed()
        except:
            return False

    def click_change_password_button(self):
        self.change_password_button.click()

    def enter_current_password(self, password):
        self.current_password_input.send_keys(password)

    def enter_new_password_twice(self, new_password):
        self.new_password_input_1.send_keys(new_password)
        self.new_password_input_2.send_keys(new_password)
