from behave import *
from pages.login import *


@when('User enters credentials')
def step_impl(context):
    page = LoginPage(context)
    page.enter_username('username')
    page.enter_password('password')


@when('User clicks Login button')
def step_impl(context):
    page = LoginPage(context)
    page.click_login_button()


@then('User is logged in')
def step_impl(context):
    page = LoginPage(context)
    assert page.after_logging_page_is_opened()
    print('User logged in as: ' + page.get_user_logged_in())


@then('Login page is opened')
def step_impl(context):
    assert 'logowanie' in context.browser.current_url
