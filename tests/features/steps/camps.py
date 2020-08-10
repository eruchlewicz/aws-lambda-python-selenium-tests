from behave import step

from pages import CampPage


@step('Camp page is opened')
def step_impl(context):
    assert 'turnusy' in context.browser.current_url
    page = CampPage(context)
    assert page.camps_page_is_displayed()
