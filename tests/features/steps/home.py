from behave import step

from environment import get_from_config
from pages import HomePage


@step('Home page is opened')
def step_impl(context):
    page = HomePage(context)
    page.visit(get_from_config('url'))
    assert get_from_config('url') in context.browser.current_url
