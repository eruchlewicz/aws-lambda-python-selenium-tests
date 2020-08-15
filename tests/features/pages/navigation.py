from selenium.webdriver.common.by import By

from .base_page_object import *


class NavigationPage(BasePage):

    def __init__(self, context):
        BasePage.__init__(
            self,
            context.browser,
            base_url=get_from_config('url'))

    locator_dictionary = {
        'login_button': (By.XPATH, '//a[@name="login_href"]'),
        'logged_user': (By.XPATH, '//li/span[contains(text(), "Witaj")]'),
        'account_button': (By.XPATH, '//a[text()="Konto"]'),
        'events_button': (By.XPATH, '//a[text()="Wydarzenia"]'),
        'camps_button': (By.XPATH, '//a[text()="Turnusy"]'),
        'retreats_button': (By.XPATH, '//a[text()="Rekolekcje"]'),
        'workshops_button': (By.XPATH, '//a[text()="Warsztaty"]'),
        'calendar_button': (By.XPATH, '//a[text()="Kalendarz"]'),
        'files_button': (By.XPATH, '//a[text()="Pliki"]'),
        'logout_button': (By.XPATH, '//a[text()="Wyloguj"]'),
    }

    def click_account_button(self):
        self.account_button.click()

    def click_events_button(self):
        self.events_button.click()

    def click_camps_button(self):
        self.camps_button.click()

    def click_retreats_button(self):
        self.retreats_button.click()

    def click_workshops_button(self):
        self.workshops_button.click()

    def click_calendar_button(self):
        self.calendar_button.click()

    def click_files_button(self):
        self.files_button.click()

    def click_logout_button(self):
        self.logout_button.click()

    def open_login_page(self):
        try:
            self.login_button.click()
        except:
            print(f'User is already logged in as: {self.logged_user.text.strip("Witaj, ")}')
