# How to Run Selenium BDD Tests in Parallel with AWS Lambda

## Step by step

Part 1: https://grapeup.com/blog/how-to-run-selenium-bdd-tests-in-parallel-with-aws-lambda/

Part 2: https://grapeup.com/blog/how-to-run-selenium-bdd-tests-in-parallel-lambda-handlers/

If you have any issues with Lambda modules, clear `selenium_layer/selenium/python/lib/python3.6/site-packages` directory and install all packeges from `requirements.txt` in this location with command:

`pip install -t selenium_layer/selenium/python/lib/python3.6/site-packages allure-behave==2.8.6`

then re-deploy all modules.
