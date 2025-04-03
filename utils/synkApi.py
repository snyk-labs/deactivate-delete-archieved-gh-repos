import json
import requests
from requests.exceptions import HTTPError
import time

from utils.tokenReader import get_snyk_token

SNYK_TOKEN = get_snyk_token()

restHeaders = {'Content-Type': 'application/vnd.api+json', 'Authorization': f'token {SNYK_TOKEN}'}
restExportHeaders = {'Content-Type': 'application/json', 'Authorization': f'token {SNYK_TOKEN}'}
v1Headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': f'token {SNYK_TOKEN}'}
rest_version = '2024-10-15'

# Paginate through Snyk's API endpoints with retry and backoff
def snyk_rest_endpoint(url, method, tenant, headers=None, body=None, return_body=False):
    match method.upper():
        case 'POST':
            try:
                response = requests.post(url, headers=headers, json=body)
                response.raise_for_status()  # Raise an error for bad responses
                # Return the body if include_body is true, otherwise return the status code
                return response.json() if return_body else response.status_code
            except requests.exceptions.RequestException as e:
                return f"An error occurred during POST request: {e}"

        case 'GET':
            try:
                results = []
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an error for bad responses
                data = response.json()
                
                # Collect data from the first page
                results.extend(data['data'])
                
                # Check for the 'next' link
                next_url = data.get('links', {}).get('next')
                
                if not next_url:
                    # If no 'next' link, return the collected results immediately
                    return data
                
                # If there is a 'next' link, continue pagination
                while next_url:
                    next_url = f'https://{tenant}' + next_url
                    response = requests.get(next_url, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    results.extend(data['data'])
                    next_url = data.get('links', {}).get('next')
                
                return results
            except requests.exceptions.RequestException as e:
                return f"An error occurred during GET request: {e}"

        case 'DELETE':
            try:
                response = requests.delete(url, headers=headers)
                response.raise_for_status()  # Raise an error for bad responses
                return response.status_code
            except requests.exceptions.RequestException as e:
                return f"An error occurred during DELETE request: {e}"

def get_snyk_targets(tenant, orgId):
    url = f'https://{tenant}/rest/orgs/{orgId}/targets?version={rest_version}'

    try:
        targetsApiResponse = snyk_rest_endpoint(url, 'GET', tenant, restHeaders)
        return targetsApiResponse
    except HTTPError as exc:
        # Raise an error
        print("Snyk Targets endpoint failed.")
        print(exc)

def get_snyk_projects_by_target_id(tenant, orgId, targetId):
    url = f'https://{tenant}/rest/orgs/{orgId}/projects?version={rest_version}&target_id={targetId}'

    try:
        projectsApiResponse = snyk_rest_endpoint(url, 'GET', tenant, restHeaders)
        return projectsApiResponse
    except HTTPError as exc:
        print("Snyk Projects endpoint failed.")
        print(exc)
        
def deactivate_project(tenant, orgId, projectId):
    url = f'https://{tenant}/v1/org/{orgId}/project/{projectId}/deactivate'

    try:
        deactivateResponse = snyk_rest_endpoint(url, 'POST', tenant, restHeaders, body={})
        return deactivateResponse
    except HTTPError as exc:
        print("Snyk Deactivate Project endpoint failed.")
        print(exc)  

def delete_project(tenant, orgId, projectId):
    url = f'https://{tenant}/rest/orgs/{orgId}/projects/{projectId}?version={rest_version}'

    try:
        deleteResponse = snyk_rest_endpoint(url, 'DELETE', tenant, restHeaders)
        return deleteResponse
    except HTTPError as exc:
        print("Snyk Delete Project endpoint failed.")
        print(exc)