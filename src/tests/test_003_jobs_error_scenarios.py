import requests
from src.conf.projectconf import Project
from src.util.requestsUtility import RequestsUtility
import logging as logger

from src.util.utilities import Utilities


def test_get_job_error_not_found(create_workflow):
    logger.info("Get a job which is not available in the project")
    workflow_id, token = create_workflow
    job_id = '00e35ab9-59d7-4a30-ae73-e1eab7b08d0e'  # Non-existent job id
    endpoint = Project.project_id + '/jobs' + job_id
    response = RequestsUtility.get(endpoint, token, 404)
    assert response['error'] == 'Not Found'  # Official docs have a detailed error msg, so either it is a
    # bug or docs need update


def test_create_and_run_job_error_incorrect_specs(create_tasks):
    logger.info("Run a job with incorrect specs")
    workflow_id, token = create_tasks
    with open("src/data/errortask.json") as f:
        data = f.read()
    response = Utilities.create_and_run_job(workflow_id, token, data=data, expected_status_code=400)
    assert "Task nasa-modis:1 does not match schema" in response['error']['message']


def test_run_job_error_too_many_jobs(create_tasks):
    logger.info("Run a job until we hit too many jobs error")
    workflow_id, token = create_tasks
    response = Utilities.create_and_run_job(workflow_id, token)
    job_id = response['data']['id']
    url = Project.base_url + Project.project_id + '/workflows/' + workflow_id + '/jobs/' + job_id
    data = {}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
    while True:
        logger.info("Running job again")
        response = requests.post(url=url, data=data, headers=headers)
        if response.status_code == 429:
            print("Too many jobs with same job ID")
            break
