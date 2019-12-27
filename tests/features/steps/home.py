from behave import *
from pages.home import *
from environment import *


@given('Home page is opened')
def step_impl(context):
    page = HomePage(context)
    page.visit(get_url_from_config())
    assert get_url_from_config() in context.browser.current_url


@when('User opens Login page')
def step_impl(context):
    page = HomePage(context)
    page.open_login_page()
