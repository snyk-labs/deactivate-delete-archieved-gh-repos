import typer
import json

from utils.githubApi import get_archived_repos_urls
from utils.tokenReader import get_github_token
from utils.synkApi import get_snyk_targets, get_snyk_projects_by_target_id, deactivate_project, delete_project
from utils.fileReader import write_json_to_file

GITHUB_TOKEN = get_github_token()

app = typer.Typer()

def find_matching_targets(archived_repo_urls, snyk_targets):
    matching_targets = []
    for target in snyk_targets:
        try:
            target_url = target.get("attributes", {}).get("url")
        except:
            print(f"Error getting target URL for {target}")
        if target_url in archived_repo_urls:
            matching_targets.append({
                "snyk_target_id": target.get("id"),
                "url": target_url
            })
    return matching_targets

def get_all_projects(matching_targets, snyk_org_id):
    all_projects = []
    for target in matching_targets:
        projects = get_snyk_projects_by_target_id(snyk_org_id, target.get("snyk_target_id"))
        # Check if projects is a dictionary and contains 'data'
        if isinstance(projects, dict) and 'data' in projects:
            all_projects.extend(projects['data'])
        else:
            all_projects.extend(projects)
            
    return all_projects

@app.command()
def generate_archived_repos_json(
    github_org_name: str = typer.Option(..., "--github-org-name", "-g", help="The name of the GitHub organization to search for archived repos"),
    snyk_org_id: str = typer.Option(..., "--snyk-org-id", "-s", help="The ID of the Snyk organization to search for targets"),
    output_file: str = typer.Option("archived-projects.json", "--output-file", "-o", help="The file path to write the JSON data")
):
    archived_repo_urls = get_archived_repos_urls(github_org_name, GITHUB_TOKEN)
    snyk_targets = get_snyk_targets(snyk_org_id)
    all_projects = []

    # Find matching Snyk targets
    print(f"Finding matching targets for archived repos in Snyk...")
    matching_targets = find_matching_targets(archived_repo_urls, snyk_targets)
    
    # Find projects by target id
    print(f"Finding projects by target id...")
    all_projects = get_all_projects(matching_targets, snyk_org_id)

    # Write matching targets to a JSON file
    write_json_to_file(all_projects, output_file)

@app.command()
def deactivate_from_json(
    input_file: str = typer.Option(..., "--input-file", "-i", help="The file path to read the JSON data from"),
):
    """Read JSON data from a file and perform deactivation."""
    try:
        with open(input_file, 'r') as json_file:
            project_data = json.load(json_file)
            for project in project_data:
                print(f"Deactivating target: {project['id']} with URL: {project['attributes']['name']}")
                deactivate_project(project['relationships']['organization']['data']['id'], project['id'])
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
    except json.JSONDecodeError as e:
        print(f"An error occurred while decoding JSON: {e}")
        
@app.command()
def delete_from_json(
    input_file: str = typer.Option(..., "--input-file", "-i", help="The file path to read the JSON data from"),
):
    """Read JSON data from a file and perform delete."""
    try:
        with open(input_file, 'r') as json_file:
            project_data = json.load(json_file)
            for project in project_data:
                print(f"Deleting target: {project['id']} with URL: {project['attributes']['name']}")
                delete_project(project['relationships']['organization']['data']['id'], project['id'])
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
    except json.JSONDecodeError as e:
        print(f"An error occurred while decoding JSON: {e}")

if __name__ == "__main__":
    app()