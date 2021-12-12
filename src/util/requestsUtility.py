import requests
from urllib3.exceptions import ProtocolError

from src.conf.projectconf import Project

"""
RequestsUtility is a wrapper class for HTTP methods
"""
class RequestsUtility:
    @staticmethod
    def post(endpoint, token, payload=None, expected_status_code=200, headers=None):
        if not headers:
            headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        url = Project.base_url + endpoint
        try:
            response = requests.post(url=url, data=payload, headers=headers)
        except KeyError:
            raise Exception("JSON Format not valid")
        except ProtocolError:
            raise Exception("Remote host closed connection forcibly")
        except Exception:
            raise Exception("Could not process request")

        status_code = response.status_code
        assert status_code == expected_status_code, \
            f'Expected {expected_status_code} but got {status_code}'
        if status_code != 204:
            return response.json()

    @staticmethod
    def put(endpoint, token, payload=None, expected_status_code=200):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        url = Project.base_url + endpoint
        try:
            response = requests.put(url=url, data=payload, headers=headers)
        except KeyError:
            raise Exception("JSON Format not valid")
        except ProtocolError:
            raise Exception("Remote host closed connection forcibly")
        except Exception:
            raise Exception("Could not process request")
        status_code = response.status_code
        assert status_code == expected_status_code, \
            f'Expected {expected_status_code} but got {status_code}'

        return response.json()

    @staticmethod
    def get(endpoint, token, expected_status_code=200):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        url = Project.base_url + endpoint
        try:
            response = requests.get(url=url, headers=headers)
        except KeyError:
            raise Exception("JSON Format not valid")
        except ProtocolError:
            raise Exception("Remote host closed connection forcibly")
        except Exception:
            raise Exception("Could not process request")
        status_code = response.status_code
        assert status_code == expected_status_code, \
            f'Expected {expected_status_code} but got {status_code}'

        return response.json()

    @staticmethod
    def delete(endpoint, token, expected_status_code=204):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}
        url = Project.base_url + endpoint
        try:
            response = requests.delete(url=url, headers=headers)
        except ProtocolError:
            raise Exception("Remote host closed connection forcibly")
        except Exception:
            raise Exception("Could not process request")
        status_code = response.status_code
        assert status_code == expected_status_code, \
            f'Expected {expected_status_code} but got {status_code}'
