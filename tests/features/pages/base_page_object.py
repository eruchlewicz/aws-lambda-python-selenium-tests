import time
import traceback

from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from environment import get_from_config


class BasePage(object):

    def __init__(self, browser, base_url=get_from_config('url')):
        self.base_url = base_url
        self.browser = browser
        self.timeout = 10

    def find_element(self, *loc):
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(loc))
        except Exception as e:
            print("Element not found", e)
        return self.browser.find_element(*loc)

    def find_elements(self, *loc):
        try:
            WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(loc))
        except Exception as e:
            print("Element not found", e)
        return self.browser.find_elements(*loc)

    def visit(self, url):
        self.browser.get(url)

    def hover(self, element):
        ActionChains(self.browser).move_to_element(element).perform()
        time.sleep(5)

    def __getattr__(self, what):
        try:
            if what in self.locator_dictionary.keys():
                try:
                    WebDriverWait(self.browser, self.timeout).until(
                        EC.presence_of_element_located(self.locator_dictionary[what])
                    )
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()

                return self.find_element(*self.locator_dictionary[what])
        except AttributeError:
            super(BasePage, self).__getattribute__("method_missing")(what)

    def method_missing(self, what):
        print("No %s here!", what)
