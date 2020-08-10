from behave import step

from environment import get_from_config
from pages import LoginPage, HomePage, NavigationPage


@step('User enters credentials')
def step_impl(context):
    page = LoginPage(context)
    page.enter_username('username')
    page.enter_password('password')


@step('User clicks Login button')
def step_impl(context):
    page = LoginPage(context)
    page.click_login_button()


@step('Login page is opened')
def step_impl(context):
    assert 'logowanie' in context.browser.current_url


@step("User is logged in")
def step_impl(context):
    home_page = HomePage(context)
    home_page.visit(get_from_config('url'))
    navigation_page = NavigationPage(context)
    navigation_page.open_login_page()
    login_page = LoginPage(context)
    login_page.enter_username('test_user')
    login_page.enter_password('test_password_123')
    login_page.click_login_button()
