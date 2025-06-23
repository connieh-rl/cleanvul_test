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

import requests
import ast

def get_changed_python_functions(commit_url):
    # Extract owner, repo, and sha
    parts = commit_url.strip("/").split("/")
    owner, repo, _, sha = parts[-4], parts[-3], parts[-2], parts[-1]

    # Get commit details
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    commit_data = requests.get(api_url).json()

    functions = {}

    for file in commit_data.get("files", []):
        filename = file.get("filename")
        if not filename.endswith(".py"):
            continue  # Only analyze Python files

        # Download the raw file (post-commit version)
        raw_url = file.get("raw_url")
        if not raw_url:
            continue

        raw_code = requests.get(raw_url).text

            #raw_code = requests.get(raw_url).text
        print(f"Downloaded {filename}, {len(raw_code)} chars")

        try:
            tree = ast.parse(raw_code)
            funcs = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            functions[filename] = funcs
        except SyntaxError:
            continue  # Skip files with invalid syntax

    return functions

# Example usage
commit_url = "https://github.com/python/cpython/commit/8d2c7d1e937b59ae3a9b315b8a51c83ab2953bf6"
funcs = get_changed_python_functions(commit_url)

# Example usage
commit_url = "https://github.com/elastic/elasticsearch/commit/8de1710b7904192195a99ec14322e6996934a0df"
message = get_commit_message_from_url(commit_url)
print("Commit message:")
print(message)
print("\nChanged Python functions:")
print(get_changed_python_functions(commit_url))