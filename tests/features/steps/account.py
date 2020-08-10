from behave import step

from pages import AccountPage


@step("Account page is opened")
def step_impl(context):
    page = AccountPage(context)
    assert page.account_page_is_opened()


@step("User data is displayed")
def step_impl(context):
    page = AccountPage(context)
    assert page.user_data_is_displayed('TestName')
    assert page.user_data_is_displayed('TestSurname')


@step("Change password button is displayed")
def step_impl(context):
    page = AccountPage(context)
    assert page.change_password_button_is_displayed()


@step("User clicks Change Password button")
def step_impl(context):
    page = AccountPage(context)
    page.click_change_password_button()


@step("Change password page is opened")
def step_impl(context):
    page = AccountPage(context)
    assert page.change_password_page_is_opened()


@step("User enters current password '{password}'")
def step_impl(context, password):
    page = AccountPage(context)
    page.enter_current_password(password)


@step("User enters new password twice '{password}'")
def step_impl(context, password):
    page = AccountPage(context)
    page.enter_new_password_twice(password)
