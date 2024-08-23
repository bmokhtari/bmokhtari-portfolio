import requests
import json
import base64
from github import Github
from datetime import datetime

# Your GitHub username
username = "bmokhtari"

# Your GitHub personal access token
access_token = "YOUR_GITHUB_ACCESS_TOKEN"

# Create a GitHub instance
g = Github(access_token)

# Get the user
user = g.get_user(username)

# Get all public repositories
repos = user.get_repos(type='public')

# Create a list to store repository information
repo_list = []

for repo in repos:
    # Skip forked repositories
    if repo.fork:
        continue
    
    repo_info = {
        "name": repo.name,
        "description": repo.description,
        "url": repo.html_url,
        "language": repo.language,
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "created_at": repo.created_at.strftime("%Y-%m-%d"),
        "last_updated": repo.updated_at.strftime("%Y-%m-%d")
    }
    repo_list.append(repo_info)

# Sort repositories by last update date
repo_list.sort(key=lambda x: datetime.strptime(x['last_updated'], "%Y-%m-%d"), reverse=True)

# Create the README content
readme_content = f"# My GitHub Projects\n\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

for repo in repo_list:
    readme_content += f"## [{repo['name']}]({repo['url']})\n\n"
    if repo['description']:
        readme_content += f"{repo['description']}\n\n"
    readme_content += f"- Language: {repo['language'] if repo['language'] else 'Not specified'}\n"
    readme_content += f"- Stars: {repo['stars']}\n"
    readme_content += f"- Forks: {repo['forks']}\n"
    readme_content += f"- Created: {repo['created_at']}\n"
    readme_content += f"- Last updated: {repo['last_updated']}\n\n"

# Update the README file in the portfolio repository
portfolio_repo = g.get_repo(f"{username}/portfolio")
readme_file = portfolio_repo.get_contents("README.md")
portfolio_repo.update_file("README.md", "Update project portfolio", readme_content, readme_file.sha)

print("Portfolio updated successfully!")
