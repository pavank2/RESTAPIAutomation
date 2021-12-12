
# REST API Automation Suite

## Summary

- The project has been implemented using Python's Pytest library.

There are 4 test files in "src.tests" directory and a conftest.py file, with a total of 16 tests
 - conftest.py: It contains 2 pytest fixtures which get invoked before each test without needing to import them.
   These fixtures are for workflow creation and  tasks creation
- test_001_workflows_happypath.py: Contains 3 additional happy path tests for workflow
- test_002_jobs_happypath.py : Contains 6 happy path tests for jobs
- test_003_jobs_error_scenarios.py : Contains 3 negative tests for jobs
- test_004_workflows_error_scenarios.py: Contains 4 negative tests for workflow

## Prerequisites
Ensure Python 3 and PIP are installed.  
Used configuration: Python 3.8.8, PIP 21.3.1

## Instructions to execute the Automation Suite

1. Create a project in up42.com and add the project ID and project key to this project.
   Navigate to src\conf\projectconf.py and update below fields:
    project_id = <your_project_id>
    project_key = <your_project_key> 

2. On a NEW terminal, clone the Automation project to your local machine

   - **git clone https://github.com/pavank2/RESTAPIAutomation.git**

2. Create a Python virtual environment of the same name 

   - **python -m venv RESTAPIAutomation**
   - **cd RESTAPIAutomation**

3. Install the libraries.
   
   - **pip install -r requirements.txt**
 
4. Run the tests!

   - **python -m pytest** (Runs all tests)
   OR
   - **python -m pytest src\tests\<filename>** (On windows; Runs individual files)  
   
   (Optionally add '--html=report.html' for a neat looking Report)
 

If something doesn't work, please feel free to contact me :-)
