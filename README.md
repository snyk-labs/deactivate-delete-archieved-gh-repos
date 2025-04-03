# Find and Deactivate GitHub Archived Repos in Snyk

This tool helps you identify archived repositories in GitHub that are also imported into Snyk. It will generate a JSON file with matching projects and provides a command to deactivate or delete them in Snyk.

## Prerequisites

- Python 3.10.14 or higher
- [Typer](https://typer.tiangolo.com/) for command-line interface
- [Requests](https://docs.python-requests.org/en/master/) for HTTP requests

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Install Dependencies**

   It's recommended to use a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Variables**

   Ensure you have the following environment variables set:

   - `GITHUB_TOKEN`: Your GitHub personal access token.
   - `SNYK_TOKEN`: Your Snyk API token.

## Usage

### Generate Archived Repositories JSON

This command generates a JSON file containing Snyk projects that match archived GitHub repositories.

```bash
python index.py generate-archived-repos-json --github-org-name <GITHUB_ORG_NAME> --snyk-org-id <SNYK_ORG_ID> [--output-file <OUTPUT_FILE>] [--snyk-tenant <SNYK_TENANT>]
```

- `--github-org-name` or `-g`: The name of the GitHub organization to search for archived repos.
- `--snyk-org-id` or `-s`: The ID of the Snyk organization to search for targets.
- `--output-file` or `-o`: (Optional) The file path to write the JSON data. Defaults to `archived-projects.json`.
- `--snyk-tenant` or `-st`: (Optional) The tenant of the Snyk organization. Defaults to `api.us.snyk.io`.

### Deactivate Projects from JSON

This command reads a JSON file and deactivates the corresponding projects in Snyk.

```bash
python index.py deactivate-from-json --input-file <INPUT_FILE> [--snyk-tenant <SNYK_TENANT>]
```

- `--input-file` or `-i`: The file path to read the JSON data from.
- `--snyk-tenant` or `-st`: (Optional) The tenant of the Snyk organization. Defaults to `api.us.snyk.io`.

### Delete Projects from JSON

This command reads a JSON file and deletes the corresponding projects in Snyk.

```bash
python index.py delete-from-json --input-file <INPUT_FILE> [--snyk-tenant <SNYK_TENANT>]
```

- `--input-file` or `-i`: The file path to read the JSON data from.
- `--snyk-tenant` or `-st`: (Optional) The tenant of the Snyk organization. Defaults to `api.us.snyk.io`.

## Example

Generate a JSON file of archived projects:

```bash
python index.py generate-archived-repos-json -g my-github-org -s my-snyk-org
```

Deactivate projects from the generated JSON file:

```bash
python index.py deactivate-from-json -i archived-projects.json
```

Delete projects from the generated JSON file:

```bash
python index.py delete-from-json -i archived-projects.json
```
