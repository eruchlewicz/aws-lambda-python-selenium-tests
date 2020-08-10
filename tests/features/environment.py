import json
import os
import platform
from datetime import date, datetime

import boto3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

REPORTS_BUCKET = 'selenium-test-reports'
SCREENSHOTS_FOLDER = 'failed_scenarios_screenshots/'
CURRENT_DATE = str(date.today())
DATETIME_FORMAT = '%H_%M_%S'


def get_from_config(what):
    if 'Linux' in platform.system():
        with open('/opt/config.json') as json_file:
            data = json.load(json_file)
            return data[what]
    elif 'Darwin' in platform.system():
        with open(os.getcwd() + '/features/config.json') as json_file:
            data = json.load(json_file)
            return data[what]
    else:
        with open(os.getcwd() + '\\features\\config.json') as json_file:
            data = json.load(json_file)
            return data[what]


def set_linux_driver(context):
    """
    Run on AWS
    """
    print("Running on AWS (Linux)")
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

    context.browser = webdriver.Chrome(
        '/opt/chromedriver', chrome_options=options, desired_capabilities=capabilities
    )


def set_windows_driver(context):
    """
    Run locally on Windows
    """
    print('Running on Windows')
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1280,1000')
    options.add_argument('--headless')
    context.browser = webdriver.Chrome(
        os.path.dirname(os.getcwd()) + '\\driver\\chromedriver.exe', chrome_options=options
    )


def set_mac_driver(context):
    """
    Run locally on Mac
    """
    print("Running on Mac")
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1280,1000')
    options.add_argument('--headless')
    context.browser = webdriver.Chrome(
        os.path.dirname(os.getcwd()) + '/driver/chromedriver', chrome_options=options
    )


def set_driver(context):
    if 'Linux' in platform.system():
        set_linux_driver(context)
    elif 'Darwin' in platform.system():
        set_mac_driver(context)
    else:
        set_windows_driver(context)


def before_all(context):
    set_driver(context)


def after_all(context):
    context.browser.quit()


def after_scenario(context, scenario):
    if scenario.status == 'failed':
        print('Scenario failed!')
        current_time = datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'{scenario.name.replace(" ", "_")}-{current_time}.png'
        if 'Linux' in platform.system():
            context.browser.save_screenshot(f'/tmp/{file_name}')
            boto3.resource('s3').Bucket(REPORTS_BUCKET).upload_file(
                f'/tmp/{file_name}', f'{SCREENSHOTS_FOLDER}{CURRENT_DATE}/{file_name}'
            )
        else:
            if not os.path.exists(SCREENSHOTS_FOLDER):
                os.makedirs(SCREENSHOTS_FOLDER)
            context.browser.save_screenshot(f'{SCREENSHOTS_FOLDER}/{file_name}')
