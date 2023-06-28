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


def issues_month(star_date: str, end_date: str):
    
    months_list = pd.period_range(start =star_date,end=end_date, freq='M')
    months_list = [month.strftime("%b-%Y") for month in months_list]

    issues = repo.get_commits()
    
    count=0

    for issue in issues:
        issue_date = issue.commit.author.date
        issue_date_str = datetime.strftime(issue_date, "%m-%d-%Y")
        if issue_date_str >= star_date and issue_date_str <= end_date:
            count+=1
    print(count)


def calculate_commit_average(star_date: str, end_date: str):

    commits = repo.get_commits()
    
    commits_count = defaultdict(int)
    
    for commit in commits:
        commit_date = commit.commit.author.date
        commit_date_str = datetime.strftime(commit_date, "%m-%d-%Y")
        if commit_date_str >= star_date and commit_date_str <= end_date:
            author = commit.author
            name = author.login if author else "Unknown"
        
            # Incrementa o numero de commits do autor
            commits_count[name] += 1
        

    total_commits = sum(commits_count.values())
    qtd_user = len(commits_count)

    average_total = total_commits / qtd_user

    data = {'Author': [], 'Commits': []}

    for author, num_commits in commits_count.items():
        data['Author'].append(author)
        data['Commits'].append(num_commits)
    
    df = pd.DataFrame(data)
    df = df.sort_values(by='Commits', ascending=False)

    print(df)

    df['Average'] = average_total # df da media total

    # Plotar um gráfico com as média de cada user

    plt.bar(df['Author'], df['Commits'])
    plt.axhline(y=average_total, color='r', linestyle='-', label='Average')
    plt.xlabel('Author')
    plt.ylabel('Commits')
    plt.title('Commits per Author')
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    return df

def check_extension(star_date: str, end_date: str):
    try:
        extension_by_author = defaultdict(lambda: defaultdict(list))
        
        commits = repo.get_commits()

        for commit in commits:
            commit_date = commit.commit.author.date
            commit_date_str = datetime.strftime(commit_date, "%m-%d-%Y")
            if commit_date_str >= star_date and commit_date_str <= end_date:
                author = commit.author.login
                file_modify = commit.files

            for file in file_modify:
                extension = file.filename.split('.')[-1]
                filename = file.filename

                extension_by_author[author][extension].append(filename)
        
        content = '## File Extensions Report by Author\n\n'

        for author, extensions in extension_by_author.items():
            content += f'## Author: {author} \n\n'
            content += '| Extension / Files |\n'
            content += '| -------- | \n'
            for extension, files in extensions.items():
                file_list = '| \n'.join(files)
                content += f'| **{extension}** | \n'
                content += f' {file_list} | \n'
            content += "\n"

        output = 'arquivo.md'

        with open(output, 'w', encoding='utf-8') as f:
            f.write(content)

    except Exception as e:
        print(f'Ocorreu um erro: {e}')

    return content

def get_coAuthor(star_date: str, end_date: str):
    coauthors = []
    hashes = []
    authors = []
    
    commits = repo.get_commits()

    for commit in commits:
        commit_date = commit.commit.author.date
        commit_date_str = datetime.strftime(commit_date, "%m-%d-%Y")
        if commit_date_str >= star_date and commit_date_str <= end_date:
            commit_message = commit.commit.message
        
        if 'Co-authored-by:' in commit_message:
            hashes.append(commit.commit.sha[:6])
            authors.append(commit.commit.author.name)

            lines = commit_message.splitlines()
            aux=[]
            for line in lines:
                if line.startswith('Co-authored-by:'):
                    aux.append(line[16:].strip().split('<')[0])
            coauthors.append(aux)

    df = pd.DataFrame({"authors": authors,"co-authors":coauthors}, index=hashes)
    
    return df