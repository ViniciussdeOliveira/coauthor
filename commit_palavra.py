from github import Github
import base64
import pandas as pd
import re


acess_token="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"

g=Github(acess_token)

repo = g.get_repo("fga-eps-mds/2023.1-RelatorioGitPython")


def commit_palavra(string: str):

    hashes = []
    messages = []
    authors = []
  
    commits = repo.get_commits()

    for commit in commits:

        commit_message = commit.commit.message
        #re.search(palavra, commit_message,re.IGNORECASE)!=None:

        if string in commit_message:
            
            hashes.append(commit.sha[:6])
            authors.append(commit.commit.author.name)
            messages.append(commit.commit.message)

 
    columns = ['hash','message','author']
    df = pd.DataFrame({"message":messages, "author": authors}, index=hashes)

    return df