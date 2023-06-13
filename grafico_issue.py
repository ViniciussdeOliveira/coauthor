from github import Github
import base64
import pandas as pd
import re
import matplotlib.pyplot as plt
import datetime

#  Colocar o seu token aqui
acess_token=""

g=Github(acess_token)

repo = g.get_repo("fga-eps-mds/2023.1-RelatorioGitPython")

def issues_month(star_date: str, end_date: str):
    
    months_list = pd.period_range(start =star_date,end=end_date, freq='M')
    months_list = [month.strftime("%b-%Y") for month in months_list]

    issues = repo.get_issues(state='closed')
    
    count=[]


    for month in months_list:
        contador=0
        for issue in issues:
            if issue.pull_request is None and issue.closed_at.strftime("%b-%Y") == month:
                contador+=1
        count.append(contador)

    df = pd.DataFrame({"num_issues": count},index=months_list)    



    # print(df)
    plt.bar(months_list, df['num_issues'])
    plt.xlabel('num_issues')
    plt.ylabel('months_list')
    plt.title('Issues per month')
    plt.xticks(rotation=45)
    plt.show()