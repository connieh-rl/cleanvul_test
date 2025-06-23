import requests
from urllib.parse import urlparse

def get_commit_message_from_url(commit_url):
    # Example URL:
    # https://github.com/owner/repo/commit/sha12345...

    parsed = urlparse(commit_url)
    path_parts = parsed.path.strip('/').split('/')

    # path_parts should be: ['owner', 'repo', 'commit', 'sha']
    if len(path_parts) < 4 or path_parts[2] != "commit":
        raise ValueError("Invalid GitHub commit URL")

    owner, repo, _, sha = path_parts[:4]

    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} {response.text}")

    commit_data = response.json()
    # Commit message is nested here:
    message = commit_data.get("commit", {}).get("message", "")
    return message

# Example usage
commit_url = "https://github.com/elastic/elasticsearch/commit/8de1710b7904192195a99ec14322e6996934a0df"
message = get_commit_message_from_url(commit_url)
print("Commit message:")
print(message)