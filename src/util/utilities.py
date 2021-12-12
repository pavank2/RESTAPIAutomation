import datetime
import json
import logging as logger
import time
import requests
import pandas as pd
from src.conf.projectconf import Project
from src.util.requestsUtility import RequestsUtility

"""
Utilities Class has wrapper methods for Creation of different elements and some generic common functions
"""


class Utilities:
    @staticmethod
    def create_token():
        token_url = "https://" + Project.project_id + ":" + Project.project_key + "@api.up42.com/oauth/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(url=token_url, data={'grant_type': 'client_credentials'}, headers=headers)
        return response.json()['data']['accessToken']

    @staticmethod
    def create_workflow(token, headers=None, data=None, expected_status_code=200):
        logger.info("Creating New workflow")
        endpoint = Project.project_id + "/workflows"
        if not headers:
            headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
        if not data:
            with open("src/data/workflow.json") as f:
                data = f.read()

        response = RequestsUtility.post(endpoint, token, data, expected_status_code, headers)
        return response

    @staticmethod
    def create_and_run_job(workflow_id, token, headers=None, data=None, expected_status_code=200):
        if not headers:
            headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
        if not data:
            with open("src/data/job_params.json") as f:
                data = f.read()
        endpoint = Project.project_id + '/workflows/' + workflow_id + '/jobs'
        response = RequestsUtility.post(endpoint, token, data, expected_status_code, headers)
        return response

    """
    Function to verify job status asynchronously until it completes 
    """

    @staticmethod
    def verify_job_status(token, job_id):
        endpoint = Project.project_id + '/jobs/' + job_id
        while True:
            response = RequestsUtility.get(endpoint, token, 200)
            status = response['data']['status']
            if status == 'PENDING' or status == 'RUNNING' or status == 'NOT_STARTED':
                logger.info("Job has not completed, sleeping for 10 seconds")
                time.sleep(10)
            else:
                logger.info("Job has completed, hence exiting")
                break
        return response

    @staticmethod
    def delete_workflow(workflow_id, token):
        logger.info("Deleting workflow")
        endpoint = Project.project_id + '/workflows/' + workflow_id
        response = RequestsUtility.delete(endpoint, token)

    """
    Function to verify the time difference between element creation and current time
    """

    @staticmethod
    def calculate_time_difference(created_at):
        created_date = pd.to_datetime(created_at)
        created_date = created_date.utcnow().replace(tzinfo=None)
        current_date = datetime.datetime.utcnow()
        return created_date.strftime("%H:%M"), current_date.strftime("%H:%M")

    """
    Function to verify the task and block details in response compared to input file
    """

    @staticmethod
    def verify_response_tasks(response_list):
        with open("src/data/tasks.json") as f:
            data = f.read()

        response_tasks = []
        input_tasks = []
        response_block_ids = []
        input_block_ids = []

        for block in response_list:
            response_tasks.append(block['name'])
            response_block_ids.append(block['block']['id'])
        for block in json.loads(data):
            input_tasks.append(block['name'])
            input_block_ids.append(block['blockId'])

        assert response_tasks == input_tasks
        assert response_block_ids == input_block_ids
