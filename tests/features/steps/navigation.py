from behave import step

from pages import NavigationPage


@step('User opens Login page')
def step_impl(context):
    page = NavigationPage(context)
    page.open_login_page()


@step("User clicks Account button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_account_button()


@step("User clicks Events button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_events_button()


@step("User clicks Camps button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_camps_button()


@step("User clicks Retreats button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_retreats_button()


@step("User clicks Workshops button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_workshops_button()


@step("User clicks Calendar button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_calendar_button()


@step("User clicks Files button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_files_button()


@step("User clicks Logout button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_logout_button()
