import boto3
import argparse
import json
import base64
import os
from datetime import date
from concurrent.futures import ThreadPoolExecutor as PoolExecutor


def get_list():
    # print(os.listdir('/opt'))
    test_cases = []
    for file in os.listdir("/opt"):
        if file.endswith(".feature"):
            test_cases.append(file)
    return test_cases


def create_folder_in_bucket():
    client = boto3.client(
        's3',
        region_name='eu-central-1',
        aws_access_key_id='XXX',
        aws_secret_access_key='YYY'
    )
    new_folder_name = str(date.today())+'/'
    client.put_object(
        Bucket='failed-scenarios-screenshots',
        Body='',
        Key=new_folder_name
    )
    return new_folder_name


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
        folder = create_folder_in_bucket()
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

        return f"Passed: {stats['passed']}, Failed: {stats['failed']}, " \
            f"Passed TC: {stats['passed_tc']}, Failed TC: {stats['failed_tc']}. " \
            f"Screenshots available in " \
            f"{'https://s3.console.aws.amazon.com/s3/buckets/failed-scenarios-screenshots/' + folder}"
    else:
        return test_cases
