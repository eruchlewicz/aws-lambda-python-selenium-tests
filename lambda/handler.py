import json
import logging
import os
from datetime import datetime
from subprocess import call

import boto3
from behave.__main__ import main as behave_main

REPORTS_BUCKET = 'aws-selenium-test-reports'
DATETIME_FORMAT = '%H:%M:%S'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_run_args(event, results_location):
    test_location = f'/opt/{event["tc_name"]}'
    run_args = [test_location]
    if 'tags' in event.keys():
        tags = event['tags'].split(' ')
        for tag in tags:
            run_args.append(f'-t {tag}')
    run_args.append('-k')
    run_args.append('-f allure_behave.formatter:AllureFormatter')
    run_args.append('-o')
    run_args.append(results_location)
    run_args.append('-v')
    run_args.append('--no-capture')
    run_args.append('--logging-level')
    run_args.append('DEBUG')
    return run_args


def lambda_runner(event, context):
    suffix = datetime.now().strftime(DATETIME_FORMAT)
    results_location = f'/tmp/result_{suffix}'
    run_args = get_run_args(event, results_location)
    print(f'Running with args: {run_args}')
    # behave -t @smoke -t ~@login -k -f allure_behave.formatter:AllureFormatter -o output --no-capture

    try:
        return_code = behave_main(run_args)
        test_result = False if return_code == 1 else True

    except Exception as e:
        print(e)
        test_result = False

    response = {'test_result': test_result}

    s3 = boto3.resource('s3')

    for file in os.listdir(results_location):
        if file.endswith('.json'):
            s3.Bucket(REPORTS_BUCKET).upload_file(f'{results_location}/{file}', f'tmp_reports/{file}')

    call(f'rm -rf {results_location}', shell=True)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
