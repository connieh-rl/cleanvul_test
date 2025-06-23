import requests
from urllib.parse import urlparse
import re
import javalang
from itertools import chain

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


def extract_java_methods_javalang(code):
    methods = []
    try:
        tree = javalang.parse.parse(code)
        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            methods.append(node.name)
    except javalang.parser.JavaSyntaxError as e:
        print("Java syntax error:", e)
    except Exception as e:
        print("Parsing error:", e)
    return methods

def get_java_methods_from_commit(commit_url):
    parsed = urlparse(commit_url)
    path_parts = parsed.path.strip('/').split('/')

    # path_parts should be: ['owner', 'repo', 'commit', 'sha']
    if len(path_parts) < 4 or path_parts[2] != "commit":
        raise ValueError("Invalid GitHub commit URL")

    owner, repo, _, sha = path_parts[-4], path_parts[-3], path_parts[-2], path_parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(f"Failed to get commit: {response.status_code} {response.text}")

    commit_data = response.json()
    methods_by_file = {}

    for file in commit_data.get("files", []):
        filename = file.get("filename")
        raw_url = file.get("raw_url")
        if not raw_url or not filename.endswith(".java"):
            continue
        raw_code = requests.get(raw_url).text
        methods = extract_java_methods_javalang(raw_code)
        methods_by_file[filename] = methods

        # Remove entries where the filename includes a slash (e.g. "dir/File.java")
        #methods_by_file = {fname: methods for fname, methods in methods_by_file.items() if '/' not in fname}
        all_methods = list(chain.from_iterable(methods_by_file.values()))
    return all_methods
