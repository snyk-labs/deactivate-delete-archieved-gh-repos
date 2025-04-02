import requests


def get_archived_repos_urls(org_name, token):   
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    URL = f"https://api.github.com/orgs/{org_name}/repos"
    
    archived_repos = []
    
    page = 1

    while True:
        response = requests.get(URL, headers=headers, params={"per_page": 100, "page": page, "type": "all"})
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        repos = response.json()
        if not repos:
            break

        archived_repos.extend([repo["html_url"] for repo in repos if repo.get("archived")])
        page += 1

    print(f"Total Archived Repositories: {len(archived_repos)}")
    return archived_repos
