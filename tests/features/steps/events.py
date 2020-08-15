from behave import step

from pages import EventsPage


@step("Events page is opened")
def step_impl(context):
    page = EventsPage(context)
    assert page.events_page_is_opened()


@step("Event signup button is displayed")
def step_impl(context):
    page = EventsPage(context)
    assert page.signup_button_is_displayed()
