from selenium.webdriver.common.by import By

from .base_page_object import *


class FilesPage(BasePage):

    def __init__(self, context):
        BasePage.__init__(
            self,
            context.browser,
            base_url=get_from_config('url'))

    locator_dictionary = {
        'files_header': (By.XPATH, '//h2[text()="Przydatne pliki"]'),
    }

    def files_page_is_opened(self):
        try:
            return self.files_header.is_displayed()
        except:
            return False
