import os
import re
import sys

def get_snyk_token():
    SNYK_TOKEN = check_if_snyk_token_exist()
    
    pattern = re.compile(r'([\d\w]{8}-[\d\w]{4}-[\d\w]{4}-[\d\w]{4}-[\d\w]{12})')
    if pattern.fullmatch(SNYK_TOKEN) == None:
        print("Snyk token is not defined or not valid.")
        sys.exit()
    else:
        return SNYK_TOKEN

def get_gitlab_token():
    GITLAB_TOKEN = check_if_gitlab_token_exist()

    pattern = re.compile(r'glpat-[\d\w]{20}')
    if pattern.fullmatch(GITLAB_TOKEN) == None:
        print("GitLab token is not defined or not valid.")
        sys.exit()
    else:
        return GITLAB_TOKEN

def get_github_token():
    GITHUB_TOKEN = check_if_github_token_exist()

    pattern = re.compile(r'ghp_[\d\w]{36}')
    if pattern.fullmatch(GITHUB_TOKEN) == None:
        print("GitHub token is not defined or not valid.")
        sys.exit()
    else:
        return GITHUB_TOKEN

def check_if_github_token_exist():
    print("Checking for GitHub token environment variable")
    try:
        if os.environ.get('GITHUB_TOKEN'):
            print("Found GitHub token")
            return os.getenv('GITHUB_TOKEN')
    except:
        print("GitHub token does not exist")
        sys.exit()

def check_if_gitlab_token_exist():
    print("Checking for GitLab token environment variable")
    try:
        if os.environ.get('GITLAB_TOKEN'):
            print("Found GitLab token")
            return os.getenv('GITLAB_TOKEN')
    except:
        print("GitLab token does not exist")
        sys.exit()

def check_if_snyk_token_exist():
    print("Checking for Snyk token environment variable")
    try:
        if os.environ.get('SNYK_TOKEN'):
            print("Found snyk token")
            return os.getenv('SNYK_TOKEN')
    except:
        print("Snyk token does not exist")
        sys.exit()