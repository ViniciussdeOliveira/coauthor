from collections import defaultdict
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
from datetime import datetime
from dotenv import load_dotenv
from github import Github

load_dotenv()
#pegando o token do github
github_token = os.getenv('GITHUB_TOKEN')
#dando acesso a biblioteca
g=Github(github_token)
#pegando o token do github
repositorio = os.getenv('REPOS')
#escolhendo o repositorio a ser analisado
repo = g.get_repo("fga-eps-mds/2023.1-RelatorioGitPython")


def get_commits_por_usuario(usuario: str, start_date: str, end_date: str):
    hashes = []
    mensages = []

    commits = repo.get_commits()
    for commit in commits:
        commit_data = commit.commit.author.date
        commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
        if commit_data_str >= start_date and commit_data_str <= end_date:
            if commit.author.login.lower() == usuario.lower():
                mensages.append(commit.commit.message)
                hashes.append(commit.sha[:6])

    df = pd.DataFrame({"Título":mensages}, index=hashes)

    if df.empty is False:
        return df
    else:
        msg = "Nenhum commit com esse usuário nesse período de tempo"
        return msg

def get_usuario_commit(start_date: str, end_date: str):

    commit_usuario = []
    commits = repo.get_commits()
    for commit in commits:
        commit_data = commit.commit.author.date
        commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
        if commit_data_str >= start_date and commit_data_str <= end_date:
            author = commit.author.login
            if author in commit_usuario:
             continue

            commit_usuario.append(author)

    df = pd.DataFrame({"Usuários": commit_usuario})
    return df

def get_coAutor(start_date: str, end_date: str):
    coautores = []
    hashes = []
    autores = []

    commits = repo.get_commits()

    for commit in commits:
        commit_data = commit.commit.author.date
        commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
        if commit_data_str >= start_date and commit_data_str <= end_date:
            commit_message = commit.commit.message

            if 'Co-authored-by:' in commit_message:
                hashes.append(commit.commit.sha[:6])
                autores.append(commit.commit.author.name)

                lines = commit_message.splitlines()
                aux=[]
                for line in lines:
                    if line.startswith('Co-authored-by:'):
                        aux.append(line[16:].strip().split('<')[0])
                coautores.append(aux)

    df = pd.DataFrame({"autores": autores,"co-authors":coautores}, index=hashes)

    if df.empty is False:
        return df
    else:
        msg = "Nenhum commit com coautor"
        return msg


def issues_fechadas(start_date: str, end_date: str):

    lista_mes = pd.period_range(start =start_date,end=end_date, freq='M')
    lista_mes = [month.strftime("%b-%Y") for month in lista_mes]

    issues = repo.get_issues(state='closed')

    count=[]


    for mes in lista_mes:
        contador=0
        for issue in issues:
            if issue.pull_request is None and issue.closed_at.strftime("%b-%Y") == mes:
                contador+=1
        count.append(contador)

    df = pd.DataFrame({"num_issues": count},index=lista_mes)


    plt.bar(lista_mes, df['num_issues'])
    plt.xlabel('Meses')
    plt.ylabel('Issues')
    plt.title('Issues por mes')
    plt.yticks(range(0,max(df['num_issues']+1)))
    plt.xticks(rotation=13)
    plt.savefig('issues_fechadas.png', format='png')

    return df

def calcular_media_commits(start_date: str, end_date: str):

    commits = repo.get_commits()

    commits_count = defaultdict(int)

    for commit in commits:
        commit_data = commit.commit.author.date
        commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
        if commit_data_str >= start_date and commit_data_str <= end_date:
            author = commit.author
            name = author.login if author else "Unknown"

            # Incrementa o numero de commits do autor
            commits_count[name] += 1


    total_commits = sum(commits_count.values())
    qtd_usuario = len(commits_count)

    media_total = total_commits / qtd_usuario

    data = {'Autor': [], 'Commits': []}

    for autor, num_commits in commits_count.items():
        data['Autor'].append(autor)
        data['Commits'].append(num_commits)

    df = pd.DataFrame(data)
    df = df.sort_values(by='Commits', ascending=False)

    df['media'] = media_total 

    plt.bar(df['Autor'], df['Commits'])
    plt.axhline(y=media_total, color='r', linestyle='-', label='media')
    plt.xlabel('Autor')
    plt.ylabel('Commits')
    plt.title('Commits por Autor')
    plt.xticks(rotation=13)
    plt.savefig('media_commits.png', format='png')

    return df

def commit_data(data: str):
    
    commits = repo.get_commits()

    commit_data = defaultdict(lambda: defaultdict(list))

    for commit in commits:
        commit_data = commit.commit.author.date
        commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
        if commit_data_str == data:
            autor = commit.author
            if autor:
                autor_name = autor.login
            else:
                autor_name = 'Unknown'

            commit_title = commit.commit.message.splitlines()[0]

            if autor_name in commit_data:
                commit_data[autor_name].append(commit_title)
            else:
                commit_data[autor_name] = [commit_title]

    content = '#Commits do dia ' + data + '\n\n'
    for autor, titles in commit_data.items():
        content += f'## Usuário: {autor}\n'
        content += f'### Títulos do commits:\n'
        for title in titles:
            content += f'- {title}\n'
        content += '\n'

    output = 'arquivo_data.md'

    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)

    return content


def commit_palavra(string: str, start_date: str, end_date: str):

    hashes = []
    mensages = []
    autores = []

    commits = repo.get_commits()

    for commit in commits:
        commit_data = commit.commit.author.date
        commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
        if commit_data_str >= start_date and commit_data_str <= end_date:

            commit_message = commit.commit.message

            if string.lower() in commit_message.lower():

                hashes.append(commit.sha[:6])
                autores.append(commit.commit.author.name)
                mensages.append(commit.commit.message)

    df = pd.DataFrame({"message":mensages, "autor": autores}, index=hashes)

    if df.empty is False:
        return df
    else:
        msg = "Nenhum commit com essa palavra nesse período de tempo"
        return msg

def checar_arquivos(start_date: str, end_date: str):
    try:
        extensao_por_autor = defaultdict(lambda: defaultdict(list))

        commits = repo.get_commits()

        for commit in commits:
            commit_data = commit.commit.author.date
            commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
            if commit_data_str >= start_date and commit_data_str <= end_date:
                autor = commit.author.login
                file_modify = commit.files

                for file in file_modify:
                    extensao = file.filename.split('.')[-1]
                    filename = file.filename

                    extensao_por_autor[autor][extensao].append(filename)

        content = '## Extensões de Arquivos de cada autor\n\n'

        for autor, extensions in extensao_por_autor.items():
            content += f'## Autor: {autor} \n\n'
            content += '| Extensão / Arquivo |\n'
            content += '| -------- | \n'
            for extensao, files in extensions.items():
                file_list = '| \n'.join(files)
                content += f'| **{extensao}** | \n'
                content += f' {file_list} | \n'
            content += "\n"

        output = 'checar_arquivos.md'

        with open(output, 'w', encoding='utf-8') as f:
            f.write(content)

    except Exception as e:
        print(f'Ocorreu um erro: {e}')

    return content

def titulo_commits(start_date: str, end_date: str):

    commits = repo.get_commits()

    commit_titulos = defaultdict(lambda: defaultdict(list))

    for commit in commits:
        commit_data = commit.commit.author.date
        commit_data_str = datetime.strftime(commit_data, "%m-%d-%Y")
        if commit_data_str >= start_date and commit_data_str <= end_date:
            autor = commit.author
            if autor:
                autor_name = autor.login
            else:
                autor_name = 'Unknown'

            commit_title = commit.commit.message.splitlines()[0]

            if autor_name in commit_titulos:
                commit_titulos[autor_name].append(commit_title)
            else:
                commit_titulos[autor_name] = [commit_title]

    content = ''

    for autor, titles in commit_titulos.items():
        content += f'## Usuário: {autor}\n'
        content += f'### Títulos do commits:\n'
        for title in titles:
            content += f'- {title}\n'
        content += '\n'

    return content

def relatorio_basico(start_date: str, end_date: str):
    content = '## Relatório do dia: ' + start_date + ' até ' + end_date
    content += '\n\n'

    content += '### Pessoas que fizeram commits:\n\n'

    usuarios = get_usuario_commit(start_date, end_date)
    for indice, linhas in usuarios.iterrows():
        for coluna, valor in linhas.items():
            content += f'- {valor}'
            nada = {coluna}
        content += '\n\n'

    content += '# Lista dos commits:\n\n'
    content += titulo_commits(start_date, end_date)
    content += '\n\n'

    content += '# Lista de Commits com Coautor:\n\n'

    coaut = get_coAutor(start_date, end_date)

    content += '| Hash | Autor | Coautor |\n'
    content += '|------|-------|---------|\n'

    for indice, linha in coaut.iterrows():
        content += f'|{indice}'
        for coluna, valor in linha.items():
            content += f'|{valor}'
            nada = {coluna}
        content += '|\n'

    content += '\n\n'
     
    content += '# Commits por pessoa e Média Geral\n\n'
    commits = calcular_media_commits(start_date, end_date)
    graph_path = 'media_commits.png'

    content += '| Autor | Commits | Média |\n'
    content += '|-------|---------|-------|\n'

    for indice, linha in commits.iterrows():
        for coluna, valor in linha.items():
            content += f'|{valor}'
            nada = {coluna}
        content += '|\n'

    content += '\n'

    content += f'![Grafico media commit]({graph_path})\n\n'
    output = 'relatorio.md'

    with open(output, 'w', encoding='utf-8') as f:

        f.write(content)


def issues_abertas():
    issues = repo.get_issues(state='open')

    content = '## Issues Abertas Assinadas\n'

    content += '| Título | Número |\n'
    content += '|--------|--------|\n'

    for issue in issues:
        if issue.assignee:
            content += f'|{issue.title}|{issue.number}|\n'

    content += '\n\n'
    content += '## Issues Abertas Não Assinadas\n'

    content += '| Título | Número |\n'
    content += '|--------|--------|\n'

    for issue in issues:
        if not issue.assignee:
            content += f'|{issue.title}|{issue.number}|\n'

    return content
