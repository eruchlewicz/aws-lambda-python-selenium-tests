from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date, datetime
import boto3
import platform
import os


def set_linux_driver(context):
    """
    Run on AWS
    """
    print("Running on Linux")
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,1000')
    options.add_argument('--single-process')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    capabilities = webdriver.DesiredCapabilities().CHROME
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True

    context.browser = webdriver.Chrome('/opt/chromedriver', chrome_options=options, desired_capabilities=capabilities)


def set_windows_driver(context):
    """
    Run locally on Windows
    """
    print("Running on Windows")
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    context.browser = webdriver.Chrome(os.path.dirname(os.getcwd()) + '/driver/chromedriver.exe',
                                       chrome_options=options)


def set_driver(context):
    if 'Linux' in platform.system():
        set_linux_driver(context)
    else:
        set_windows_driver(context)


def before_all(context):
    set_driver(context)


def after_all(context):
    context.browser.quit()


def after_scenario(context, scenario):
    if scenario.status == "failed":
        print("Scenario failed!")
        if 'Linux' in platform.system():
            current_time = datetime.now().strftime("%H:%M:%S")
            file_name = scenario.name + str(current_time) + ".png"
            context.browser.save_screenshot('/tmp/' + file_name)
            s3 = boto3.resource(
                's3',
                aws_access_key_id='XXX',
                aws_secret_access_key='YYY'
            )
            s3.Bucket('failed-scenarios-screenshots').upload_file('/tmp/' + file_name,
                                                                  str(date.today()) + '/' + file_name)
        else:
            current_path = os.getcwd()
            if not os.path.exists("failed_scenarios_screenshots"):
                os.makedirs("failed_scenarios_screenshots")
            os.chdir("failed_scenarios_screenshots")
            context.browser.save_screenshot(scenario.name + "_failed.png")
            os.chdir(current_path)
