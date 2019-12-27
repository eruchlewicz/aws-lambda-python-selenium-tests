from behave.__main__ import main as behave_main
import json


def lambda_runner(event, context):
    test_result = True
    test_location = "/opt/" + str(event['tc_id'])
    run_args = [test_location]
    if 'tags' in event.keys():
        tags = event['tags'].split(" ")
        for tag in tags:
            run_args.append('-t ' + tag)
    run_args.append('-k')
    run_args.append('--no-capture')
    print(f"Running with args: {run_args}")
    try:
        behave_main(run_args)
    except:
        test_result = False

    response = {
        "test_result": test_result
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
