from selenium.webdriver.common.by import By

from .base_page_object import *


class CalendarPage(BasePage):

    def __init__(self, context):
        BasePage.__init__(
            self,
            context.browser,
            base_url=get_from_config('url'))

    locator_dictionary = {
        'calendar_header': (By.XPATH, '//h2[text()="Kalendarz"]'),
    }

    def calendar_page_is_opened(self):
        try:
            return self.calendar_header.is_displayed()
        except:
            return False
