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
#dando acesso a biblioteca
g=Github(github_token)
#escolhendo o repositorio a ser analisado
repo = g.get_repo("fga-eps-mds/2023.1-RelatorioGitPython")

current_working_directory = os.getcwd()
repository_path = discover_repository(current_working_directory)
repository = Repository(repository_path)