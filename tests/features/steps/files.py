from behave import step

from pages import FilesPage


@step("Files page is opened")
def step_impl(context):
    page = FilesPage(context)
    assert page.files_page_is_opened()
