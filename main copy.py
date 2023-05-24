from pygit2 import Repository, discover_repository
import os
from pygit2 import GIT_SORT_REVERSE, GIT_SORT_TIME
from pygit2 import *
import pygit2
import pandas as pd


# Abrir o repositório Git
current_working_directory = os.getcwd()
repository_path = discover_repository(current_working_directory)
repository = Repository(repository_path)

coauthors = []
hashes = []
authors = []
columns = ['hash','author','co-author']


# Obter o commit mais recente (HEAD)
commit = repository.revparse_single('HEAD')

# Percorrer todos os commits
for commit in repository.walk(commit.id, GIT_SORT_TOPOLOGICAL):
    commit_message = commit.message
    if 'Co-authored-by:' in commit_message:

        hashes.append(str(commit.hex)[:6])
        authors.append(commit.author.name)

        lines = commit.message.splitlines()
        for line in lines:
            if line.startswith('Co-authored-by:'):
                coauthors.append(line[16:].strip().split('<')[0])
               
    # Comparar a mensagem do commit com a linha "Co-authored-by"
    
    
        #print(f'O commit {commit.hex} tem coautores.{commit.author.name} {coauthors}')

df= pd.DataFrame({"authors":authors,"co-authors":coauthors},index=hashes)
print(df)


