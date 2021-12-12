import json
import logging as logger
import pytest
from src.conf.projectconf import Project
from src.util.utilities import Utilities
from src.util.requestsUtility import RequestsUtility


def test_create_and_run_job(create_tasks):
    workflow_id, token = create_tasks
    response = Utilities.create_and_run_job(workflow_id, token)
    job_id = response['data']['id']
    assert job_id is not None
    assert response['data']['createdBy']['id'] == Project.project_id
    assert response['data']['workflowId'] == workflow_id

    logger.info("Verify input tasks in response")
    with open("src/data/tasks.json") as f:
        data = f.read()
    response_tasks = []
    input_tasks = []
    for task in response['data']['inputs']:
        response_tasks.append(task)
    for task in json.loads(data):
        input_tasks.append(task['name'])
    assert response_tasks == input_tasks

    logger.info("Verify created date is same as current date")
    created_date = response['data']['createdAt']
    (created_date_utc, current_date_utc) = Utilities.calculate_time_difference(created_date)
    assert created_date_utc == current_date_utc
    logger.info("Verify job status asynchronously until it completes")
    response = Utilities.verify_job_status(token, job_id)
    assert response['data']['status'] == 'SUCCEEDED'


def test_get_jobs(create_tasks):
    logger.info("Get all jobs in a project")
    workflow_id, token = create_tasks
    response = Utilities.create_and_run_job(workflow_id, token)
    job_id = response['data']['id']
    assert job_id is not None
    endpoint = Project.project_id + '/jobs'
    response = RequestsUtility.get(endpoint, token, 200)
    num_of_jobs = len(response['data'])
    logger.info(f"Number of jobs in the project :{num_of_jobs}")


def test_rerun_job(create_tasks):
    logger.info("Rerun a job")
    workflow_id, token = create_tasks
    response = Utilities.create_and_run_job(workflow_id, token)
    job_id = response['data']['id']
    assert job_id is not None
    response = Utilities.verify_job_status(token, job_id)
    assert response['data']['status'] == 'SUCCEEDED'

    logger.info("Running job again")
    endpoint = Project.project_id + '/workflows/' + workflow_id + '/jobs/' + job_id
    data = {}
    RequestsUtility.post(endpoint, token, data, 200)
    response = Utilities.verify_job_status(token, job_id)
    assert response['data']['status'] == 'SUCCEEDED'


def test_rename_job(create_tasks):
    logger.info("Rename a job")
    workflow_id, token = create_tasks
    response = Utilities.create_and_run_job(workflow_id, token)
    job_id = response['data']['id']
    assert job_id is not None

    logger.info("Rename previously run job")
    endpoint = Project.project_id + '/workflows/' + workflow_id + '/jobs/' + job_id
    data = {"name": "MyNewJob"}
    response = RequestsUtility.put(endpoint, token, json.dumps(data), 200)
    assert response['data']['name'] == data['name']


def test_get_job_tasks(create_tasks):
    logger.info("Get tasks associated with a job")
    workflow_id, token = create_tasks
    response = Utilities.create_and_run_job(workflow_id, token)
    job_id = response['data']['id']
    assert job_id is not None, "Job not created"
    endpoint = Project.project_id + '/jobs/' + job_id + '/tasks'
    response = RequestsUtility.get(endpoint, token, 200)

    logger.info("Verify tasks in response are same as input tasks")
    Utilities.verify_response_tasks(response['data'])
    """
    with open("src/data/tasks.json") as f:
        data = f.read()
    response_tasks = []
    input_tasks = []
    for task in response['data']:
        response_tasks.append(task['name'])
    for task in json.loads(data):
        input_tasks.append(task['name'])

    assert response_tasks == input_tasks
    """

def test_cancel_job(create_tasks):
    logger.info("Cancel a job")
    workflow_id, token = create_tasks
    response = Utilities.create_and_run_job(workflow_id, token)
    job_id = response['data']['id']
    assert job_id is not None, "Job not created"
    endpoint = Project.project_id + '/jobs/' + job_id + '/cancel'
    data = {}
    response = RequestsUtility.post(endpoint, token, data, 204)
    assert response is None
