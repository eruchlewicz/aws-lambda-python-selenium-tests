import json
import logging
import os
from datetime import datetime

import boto3
from behave.__main__ import main as behave_main
from selenium.webdriver.remote.remote_connection import LOGGER


def lambda_runner(event, context):
    LOGGER.setLevel(logging.DEBUG)
    test_result = True
    now = datetime.now()
    suffix = now.strftime("%H:%M:%S")
    results_location = '/tmp/result_' + str(suffix)
    test_location = "/opt/" + str(event['tc_id'])

    run_args = [test_location]
    if 'tags' in event.keys():
        tags = event['tags'].split(" ")
        for tag in tags:
            run_args.append('-t ' + tag)
    run_args.append('-k')
    run_args.append('-f allure_behave.formatter:AllureFormatter')
    run_args.append('-o')
    run_args.append(results_location)
    run_args.append('--no-capture')
    print(f"Running with args: {run_args}")
    # behave -t @smoke -t ~@login -k -f allure_behave.formatter:AllureFormatter -o /output --no-capture

    try:
        behave_main(run_args)
    except:
        test_result = False

    response = {
        "test_result": test_result
    }

    s3 = boto3.resource(
        's3'
    )

    for file in os.listdir(results_location):
        print(file)
        if file.endswith(".json"):
            s3.Bucket('selenium-test-reports').upload_file(results_location + '/' + file, 'tmp_reports/' + file)

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
