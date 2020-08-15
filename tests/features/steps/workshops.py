from behave import step

from pages import WorkshopsPage


@step("Workshops page is opened")
def step_impl(context):
    page = WorkshopsPage(context)
    assert page.workshops_page_is_opened()


@step("Workshop signup button is displayed")
def step_impl(context):
    page = WorkshopsPage(context)
    assert page.signup_button_is_displayed()
