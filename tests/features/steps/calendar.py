from behave import step

from pages import CalendarPage


@step("Calendar page is opened")
def step_impl(context):
    page = CalendarPage(context)
    assert page.calendar_page_is_opened()
