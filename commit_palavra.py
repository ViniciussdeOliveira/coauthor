from pygit2 import Repository, discover_repository
from collections import defaultdict
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
from github import Github
from pygit2 import GIT_SORT_REVERSE, GIT_SORT_TIME
from pygit2 import *

load_dotenv()
#pegando o token do github
github_token = os.getenv('GITHUB_TOKEN')
repos = os.getenv('REPOS')
#dando acesso a biblioteca
g=Github(github_token)
#escolhendo o repositorio a ser analisado
repo = g.get_repo(repos)


def commit_palavra(string: str, start_date: str, end_date: str):

    hashes = []
    messages = []
    authors = []

    commits = repo.get_commits()

    for commit in commits:
        commit_date = commit.commit.author.date
        commit_date_str = datetime.strftime(commit_date, "%m-%d-%Y")
        if commit_date_str >= start_date and commit_date_str <= end_date:

            commit_message = commit.commit.message

            if string.lower() in commit_message.lower():

                hashes.append(commit.sha[:6])
                authors.append(commit.commit.author.name)
                messages.append(commit.commit.message)

    df = pd.DataFrame({"message":messages, "author": authors}, index=hashes)

    if df.empty is False:
        return df
    else:
        msg = "No commits with this word"
        return msg
    
def get_commits_by_user(usuario: str, start_date: str, end_date: str):
    hashes = []
    messages = []

    commits = repo.get_commits()
    for commit in commits:
        commit_date = commit.commit.author.date
        commit_date_str = datetime.strftime(commit_date, "%m-%d-%Y")
        if commit_date_str >= start_date and commit_date_str <= end_date:
            if commit.author.login.lower() == usuario.lower():
                messages.append(commit.commit.message)
                hashes.append(commit.sha[:6])

    df = pd.DataFrame({"Message":messages}, index=hashes)     

    if df.empty is False:
        return df
    else:
        msg = "No commits with this user"
        return msg


def title_commits(start_date: str, end_date: str):

    commits = repo.get_commits()

    commit_titles = defaultdict(lambda: defaultdict(list))

    for commit in commits:
        commit_date = commit.commit.author.date
        commit_date_str = datetime.strftime(commit_date, "%m-%d-%Y")
        if commit_date_str >= start_date and commit_date_str <= end_date:
            author = commit.author
            if author:
                author_name = author.login
            else:
                author_name = 'Unknown'

            commit_title = commit.commit.message.splitlines()[0]

            if author_name in commit_titles:
                commit_titles[author_name].append(commit_title)
            else:
                commit_titles[author_name] = [commit_title]

    content = '#File Title Commits\n\n'
    for author, titles in commit_titles.items():
        content += f'## Usuário: {author}\n'
        content += f'### Títulos do commits:\n'
        for title in titles:
            content += f'- {title}\n'
        content += '\n'
    
    output = 'arquivo_title.md'

    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)