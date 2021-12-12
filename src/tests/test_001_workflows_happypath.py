import json
import pytest
from src.conf.projectconf import Project
from src.util.requestsUtility import RequestsUtility
from src.util.utilities import Utilities
import logging as logger


def test_get_all_workflows(create_workflow):
    logger.info("Get all the workflows in the project")
    workflow_id, token = create_workflow
    endpoint = Project.project_id + '/workflows'
    response = RequestsUtility.get(endpoint, token, 200)
    created_date = response['data'][0]['createdAt']
    (created_date_utc, current_date_utc) = Utilities.calculate_time_difference(created_date)
    print(created_date_utc, current_date_utc)
    assert created_date_utc == current_date_utc


def test_get_specific_workflow(create_workflow):
    logger.info("Get a specific in the project")
    workflow_id, token = create_workflow
    endpoint = Project.project_id + '/workflows/' + workflow_id
    response = RequestsUtility.get(endpoint, token, 200)
    assert response['data']['id'] == workflow_id
    assert response['data']['createdBy']['id'] == Project.project_id


def test_workflow_get_tasks(create_tasks):
    logger.info("Get the tasks in a workflow")
    workflow_id, token = create_tasks
    endpoint = Project.project_id + '/workflows/' + workflow_id + '/tasks'
    response = RequestsUtility.get(endpoint, token, 200)

    logger.info("Verify tasks names and block IDs in response are same as input")
    Utilities.verify_response_tasks(response['data'])
