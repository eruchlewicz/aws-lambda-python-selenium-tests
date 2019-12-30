import boto3
import argparse
import json
import base64
import os
import shutil
import logging
from datetime import date, datetime
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
import subprocess


def get_list():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # print(os.listdir('/opt'))
    test_cases = []
    for file in os.listdir("/opt"):
        if file.endswith(".feature"):
            test_cases.append(file)
    return test_cases


def get_s3_resource():
    s3 = boto3.resource(
        's3',
        aws_access_key_id='XXX',
        aws_secret_access_key='YYY'
    )
    return s3


def get_s3_client():
    client = boto3.client(
        's3',
        aws_access_key_id='XXX',
        aws_secret_access_key='YYY'
    )
    return client


def remove_s3_folder(folder_name):
    s3 = get_s3_resource()
    bucket = s3.Bucket('selenium-test-reports')
    bucket.objects.filter(Prefix=folder_name).delete()


def create_screenshots_folder_in_bucket():
    client = get_s3_client()
    new_folder_name = str(date.today())+'/'
    client.put_object(
        Bucket='failed-scenarios-screenshots',
        Body='',
        Key=new_folder_name
    )
    return new_folder_name


def create_report_folder_in_bucket(new_folder_name):
    client = get_s3_client()
    remove_s3_folder(new_folder_name)
    client.put_object(
        Bucket='selenium-test-reports',
        Body='',
        Key=new_folder_name
    )


def upload_report_html_to_s3(report_path):
    s3 = get_s3_resource()
    current_path = os.getcwd()
    os.chdir('/tmp')
    shutil.make_archive('report', 'zip', report_path)
    s3.Bucket('selenium-test-reports').upload_file('report.zip', 'report_' + str(datetime.now()) + '.zip')
    os.chdir(current_path)


def upload_report_history_to_s3():
    s3 = get_s3_resource()
    current_path = os.getcwd()
    os.chdir('/tmp/tmp_reports/Allure/history')
    for file in os.listdir("/tmp/tmp_reports/Allure/history"):
        if file.endswith(".json"):
            s3.Bucket('selenium-test-reports').upload_file(file, 'history/' + file)
    os.chdir(current_path)


def download_folder_from_bucket(dist, bucket, local='/tmp'):
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
    test_cases = get_list()
    if event['action'] == 'run_tests':
        parser = argparse.ArgumentParser(description='Serverless test runner')
        parser.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")
        parser.add_argument("-s", "--sequentional", help="Disable parallel mode", action="store_true")
        args = parser.parse_args()
        data_dict = {'scheduled': False, 'executed': False, 'result': None, 'output': None}
        async_set = dict((d, data_dict) for d in test_cases)
        tags = event['tags']
        screenshots_folder = create_screenshots_folder_in_bucket()
        report_folder = 'tmp_reports/'
        create_report_folder_in_bucket(report_folder)
        client = boto3.client(
            'lambda',
            region_name='eu-central-1',
            aws_access_key_id='XXX',
            aws_secret_access_key='YYY'
        )

        def invoke_test(tc_name):
            async_set[tc_name]['scheduled'] = True
            # print(f" TC '{tc_name}': scheduled")
            response = client.invoke(
                FunctionName='lambda-test-runner-dev-lambda_runner',
                InvocationType='RequestResponse',
                LogType='Tail',
                Payload=f'{{"tc_id": "{tc_name}", "tags": "{tags}"}}'
            )

            async_set[tc_name]['executed'] = True
            # print(f" TC '{tc_name}': executed")
            async_set[tc_name]['output'] = response

            result = json.loads(response['Payload'].read())
            # print(result)
            result_body = json.loads(result['body'])
            async_set[tc_name]['result'] = bool(result_body['test_result'])

        if not args.sequentional:
            with PoolExecutor(max_workers=500) as executor:
                for _ in executor.map(invoke_test, async_set):
                    pass
        else:
            for tc_id in async_set:
                invoke_test(tc_id)

        stats = {'passed': 0, 'failed': 0, 'passed_tc': [], 'failed_tc': []}

        for tc_id in async_set:
            tc_data = async_set[tc_id]

            if tc_data['result']:
                stats['passed'] += 1
                stats['passed_tc'].append(tc_id)
            else:
                stats['failed'] += 1
                stats['failed_tc'].append(tc_id)

            if not tc_data or args.verbose:
                print(str(base64.b64decode(tc_data['output']['LogResult']), 'utf-8'))

        try:
            download_folder_from_bucket(report_folder, 'selenium-test-reports')
            tmp_reports_folder = '/tmp/' + report_folder
            download_folder_from_bucket('history/', 'selenium-test-reports', tmp_reports_folder)
            command_generate_allure_report = ['/opt/allure-2.10.0/bin/allure generate --clean %s -o %s/Allure/' %
                                              (tmp_reports_folder, tmp_reports_folder)]
            subprocess.call(command_generate_allure_report, shell=True)
            upload_report_html_to_s3(tmp_reports_folder + 'Allure')
            upload_report_history_to_s3()
            remove_s3_folder(report_folder)
        except:
            print("Error when generating report")

        return f"Passed: {stats['passed']}, Failed: {stats['failed']}, " \
            f"Passed TC: {stats['passed_tc']}, Failed TC: {stats['failed_tc']}. " \
            f"Screenshots available in " \
            f"{'https://s3.console.aws.amazon.com/s3/buckets/failed-scenarios-screenshots/' + screenshots_folder} " \
            f"Reports available in " \
            f"{'https://s3.console.aws.amazon.com/s3/buckets/selenium-test-reports/'}"

    else:
        return test_cases
