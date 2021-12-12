import logging as logger
import pytest
from src.util.requestsUtility import RequestsUtility
from src.conf.projectconf import Project
from src.util.utilities import Utilities

"""
conftest.py is automatically executed by pytest at the beginning of each test.
 Contains 2 pytest fixtures - one for workflow creation and another for tasks creation
"""


@pytest.fixture
def create_workflow():
    token = Utilities.create_token()
    response = Utilities.create_workflow(token)
    workflow_id = response['data']['id']
    yield workflow_id, token
    # Anything after yield is part of teardown setup
    Utilities.delete_workflow(workflow_id, token)


@pytest.fixture
def create_tasks(create_workflow):
    workflow_id, token = create_workflow
    endpoint = Project.project_id + '/workflows/' + workflow_id + '/tasks'
    logger.info("Creating New Tasks in the workflow")
    with open("src/data/tasks.json") as f:
        data = f.read()
    response = RequestsUtility.post(endpoint, token, data, 200)

    Utilities.verify_response_tasks(response['data'])

    yield workflow_id, token
