import json
import logging
import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from datetime import date, datetime

import boto3
from botocore.client import ClientError, Config

REPORTS_BUCKET = 'aws-selenium-test-reports'
SCREENSHOTS_FOLDER = 'failed_scenarios_screenshots/'
CURRENT_DATE = str(date.today())
REPORTS_FOLDER = 'tmp_reports/'
TMP_REPORTS_FOLDER = f'/tmp/{REPORTS_FOLDER}'
TMP_REPORTS_ALLURE_FOLDER = f'{TMP_REPORTS_FOLDER}Allure/'
TMP_REPORTS_ALLURE_HISTORY_FOLDER = f'{TMP_REPORTS_ALLURE_FOLDER}history/'
REGION = 'eu-central-1'

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_test_cases_list() -> list:
    return [file for file in os.listdir('/opt') if file.endswith('.feature')]


def get_s3_resource():
    return boto3.resource('s3')


def get_s3_client():
    return boto3.client('s3', config=Config(max_pool_connections=500))


def remove_s3_folder(folder_name: str):
    s3 = get_s3_resource()
    bucket = s3.Bucket(REPORTS_BUCKET)
    bucket.objects.filter(Prefix=folder_name).delete()


def create_bucket(bucket_name: str):
    client = get_s3_client()
    try:
        client.head_bucket(Bucket=bucket_name)
    except ClientError:
        location = {'LocationConstraint': REGION}
        client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)


def create_folder(bucket_name: str, folder_name: str):
    client = get_s3_client()
    client.put_object(
        Bucket=bucket_name,
        Body='',
        Key=folder_name
    )


def create_sub_folder(bucket_name: str, folder_name: str, sub_folder_name: str):
    client = get_s3_client()
    client.put_object(
        Bucket=bucket_name,
        Body='',
        Key=f'{folder_name}{sub_folder_name}'
    )


def upload_html_report_to_s3(report_path: str):
    s3 = get_s3_resource()
    current_path = os.getcwd()
    os.chdir('/tmp')
    shutil.make_archive('report', 'zip', report_path)
    s3.Bucket(REPORTS_BUCKET).upload_file('report.zip', f'report_{str(datetime.now())}.zip')
    os.chdir(current_path)


def upload_report_history_to_s3():
    s3 = get_s3_resource()
    current_path = os.getcwd()
    os.chdir(TMP_REPORTS_ALLURE_HISTORY_FOLDER)
    for file in os.listdir(TMP_REPORTS_ALLURE_HISTORY_FOLDER):
        if file.endswith('.json'):
            s3.Bucket(REPORTS_BUCKET).upload_file(file, f'history/{file}')
    os.chdir(current_path)


def download_folder_from_bucket(bucket, dist, local='/tmp'):
    s3 = get_s3_resource()
    paginator = s3.meta.client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_folder_from_bucket(subdir.get('Prefix'), bucket, local)
        for file in result.get('Contents', []):
            destination_pathname = os.path.join(local, file.get('Key'))
            if not os.path.exists(os.path.dirname(destination_pathname)):
                os.makedirs(os.path.dirname(destination_pathname))
            if not file.get('Key').endswith('/'):
                s3.meta.client.download_file(bucket, file.get('Key'), destination_pathname)


def lambda_test_list(event, context):
    test_cases = get_test_cases_list()
    if event['action'] == 'run_tests':
        tags = event['tags']
        create_bucket(bucket_name=REPORTS_BUCKET)
        create_folder(bucket_name=REPORTS_BUCKET, folder_name=SCREENSHOTS_FOLDER)
        create_sub_folder(
            bucket_name=REPORTS_BUCKET, folder_name=SCREENSHOTS_FOLDER, sub_folder_name=f'{CURRENT_DATE}/'
        )
        remove_s3_folder(folder_name=REPORTS_FOLDER)
        create_folder(bucket_name=REPORTS_BUCKET, folder_name=REPORTS_FOLDER)
        client = boto3.client('lambda', region_name=REGION)

        stats = {'passed': 0, 'failed': 0, 'passed_tc': [], 'failed_tc': []}

        def invoke_test(tc_name):
            response = client.invoke(
                FunctionName='lambda-test-runner-dev-lambda_runner',
                InvocationType='RequestResponse',
                LogType='Tail',
                Payload=f'{{"tc_name": "{tc_name}", "tags": "{tags}"}}'
            )

            result_payload = json.loads(response['Payload'].read())
            result_body = json.loads(result_payload['body'])
            test_passed = bool(result_body['test_result'])

            if test_passed:
                stats['passed'] += 1
                stats['passed_tc'].append(tc_name)
            else:
                stats['failed'] += 1
                stats['failed_tc'].append(tc_name)

        if event.get('seq'):
            for tc in test_cases:
                invoke_test(tc)
        else:
            with PoolExecutor(max_workers=500) as executor:
                for _ in executor.map(invoke_test, test_cases):
                    pass

        try:
            download_folder_from_bucket(bucket=REPORTS_BUCKET, dist=REPORTS_FOLDER)
            download_folder_from_bucket(bucket=REPORTS_BUCKET, dist='history/', local=TMP_REPORTS_FOLDER)
            command_generate_allure_report = [
                f'/opt/allure-2.10.0/bin/allure generate --clean {TMP_REPORTS_FOLDER} -o {TMP_REPORTS_ALLURE_FOLDER}'
            ]
            subprocess.call(command_generate_allure_report, shell=True)
            upload_html_report_to_s3(report_path=TMP_REPORTS_ALLURE_FOLDER)
            upload_report_history_to_s3()
            remove_s3_folder(REPORTS_FOLDER)
        except Exception as e:
            print(f'Error when generating report: {e}')

        return {
            'Passed or Skipped': stats['passed'],
            'Failed': stats['failed'],
            'Passed or Skipped TC': stats['passed_tc'],
            'Failed TC': stats['failed_tc'],
            'Screenshots': f'https://s3.console.aws.amazon.com/s3/buckets/{REPORTS_BUCKET}/'
                           f'{SCREENSHOTS_FOLDER}{CURRENT_DATE}/',
            'Reports': f'https://s3.console.aws.amazon.com/s3/buckets/{REPORTS_BUCKET}/'
        }

    else:
        return test_cases
