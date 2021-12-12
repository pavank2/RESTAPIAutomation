import json
import time
import pytest
from src.conf.projectconf import Project
from src.util.requestsUtility import RequestsUtility
from src.util.utilities import Utilities
import logging as logger


def test_create_workflow_error_empty_data():
    logger.info("Error scenario: Create workflow with no name in data")
    token = Utilities.create_token()
    with open("src/data/errordata.json") as f:  # JSON data wrong
        data = f.read()
    json_data = json.loads(data)['data']['noname']
    response = Utilities.create_workflow(token, data=json_data, expected_status_code=400)
    assert "JSON parse error" in response['error']['message']


def test_create_workflow_error_wrong_data_format():
    logger.info("Error scenario: Creating New workflow with wrong data format")
    token = Utilities.create_token()
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/xml;charset=UTF-8'}
    response = Utilities.create_workflow(token, headers=headers, expected_status_code=415)
    assert response['error']['message'] == "Content type 'application/xml;charset=UTF-8' not supported"


def test_get_specific_workflow_error_not_found():
    logger.info("Error scenario: Get a non-existent workflow")
    token = Utilities.create_token()
    workflow_id = "b16f2676-1420-4146-b000-529b9ee2b724"  # dummy workflow id
    endpoint = Project.project_id + '/workflows/' + workflow_id
    response = RequestsUtility.get(endpoint, token, 404)
    assert f"Workflow not found for id {workflow_id}" in response['error']['message']


def test_create_workflow_error_token_expired():
    logger.info("Error scenario: Creating New workflow with token expired")
    token = Utilities.create_token()
    logger.info("Sleeping for 5 min for the token to expire.Please be patient for the last test")
    time.sleep(300)
    response = Utilities.create_workflow(token, expected_status_code=401)
    assert "Unauthorized" in response['error']['message']
    # Official docs mention error message as 'ACCESS_TOKEN_EXPIRED' which seems more appropriate


