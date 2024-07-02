import requests
from requests.auth import HTTPBasicAuth
import json

# Replace 'your_github_username' and 'your_github_token' with your GitHub username and token.
GITHUB_USERNAME = 'your_github_username'
GITHUB_TOKEN = 'your_github_token'
SEARCH_QUERY = 'firewall config'
SEARCH_URL = 'https://api.github.com/search/code'
RESULTS_PER_PAGE = 30  # Maximum allowed by GitHub API

def search_github(query, per_page=RESULTS_PER_PAGE):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    params = {
        'q': query,
        'per_page': per_page,
    }
    response = requests.get(SEARCH_URL, headers=headers, params=params, auth=HTTPBasicAuth(GITHUB_USERNAME, GITHUB_TOKEN))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")

def main():
    try:
        results = search_github(SEARCH_QUERY)
        print(f"Total results: {results['total_count']}")
        for item in results['items']:
            repo_url = item['repository']['html_url']
            file_path = item['path']
            print(f"Repository: {repo_url}, File: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
