from behave import step

from pages import CampsPage


@step('Camps page is opened')
def step_impl(context):
    assert 'turnusy' in context.browser.current_url
    page = CampsPage(context)
    assert page.camps_page_is_displayed()


@step("Camp signup button is displayed")
def step_impl(context):
    page = CampsPage(context)
    assert page.signup_button_is_displayed()
