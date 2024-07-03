import os
import requests
from requests.auth import HTTPBasicAuth

# Environment variables for GitHub credentials
GIT_USERNAME = os.getenv('GIT_USERNAME')
GIT_TOKEN = os.getenv('GIT_TOKEN')

# Query parameters
SEARCH_QUERY = 'firewall config'
SEARCH_URL = 'https://api.github.com/search/code'
RESULTS_PER_PAGE = 30  # Maximum allowed by GitHub API
DOWNLOAD_DIR = 'downloaded_configs'  # Directory to store downloaded files

def search_github(query, per_page=RESULTS_PER_PAGE):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {
        'q': query,
        'per_page': per_page,
    }
    response = requests.get(SEARCH_URL, headers=headers, params=params, auth=HTTPBasicAuth(GIT_USERNAME, GIT_TOKEN))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")

def download_file(repo_url, file_path, download_dir):
    file_url = f"{repo_url}/raw/main/{file_path}"
    response = requests.get(file_url)
    if response.status_code == 200:
        local_path = os.path.join(download_dir, file_path.replace('/', '_'))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_url} to {local_path}")
    else:
        print(f"Failed to download: {file_url}")

def main():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    try:
        results = search_github(SEARCH_QUERY)
        print(f"Total results: {results['total_count']}")
        for item in results['items']:
            repo_url = item['repository']['html_url']
            file_path = item['path']
            print(f"Repository: {repo_url}, File: {file_path}")
            download_file(repo_url, file_path, DOWNLOAD_DIR)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
