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


@step("User clicks Logout button")
def step_impl(context):
    page = NavigationPage(context)
    page.click_logout_button()
