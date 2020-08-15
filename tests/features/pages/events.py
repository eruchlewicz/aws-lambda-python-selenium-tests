from selenium.webdriver.common.by import By

from .base_page_object import *


class EventsPage(BasePage):

    def __init__(self, context):
        BasePage.__init__(
            self,
            context.browser,
            base_url=get_from_config('url'))

    locator_dictionary = {
        'events_header': (By.XPATH, '//h2[text()="Moje wydarzenia"]'),
        'signup_button': (By.XPATH, '//button[@type="submit" and contains(text(), "Zapisz się")]'),
    }

    def events_page_is_opened(self):
        try:
            return self.events_header.is_displayed()
        except:
            return False

    def signup_button_is_displayed(self):
        try:
            return self.signup_button.is_displayed()
        except:
            return False
