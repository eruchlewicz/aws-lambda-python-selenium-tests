from behave import step

from pages import RetreatsPage


@step("Retreats page is opened")
def step_impl(context):
    page = RetreatsPage(context)
    assert page.retreats_page_is_opened()


@step("Retreat signup button is displayed")
def step_impl(context):
    page = RetreatsPage(context)
    assert page.signup_button_is_displayed()
