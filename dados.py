import os
import csv

arquivos = {
    "livros.csv": ["Título", "Autor", "Ano", "ISBN", "Categoria"],
    "usuarios.csv": ["ID", "Nome", "Email", "Tipo", "Livros_Emprestados"],
    "emprestimos.csv": ["Livro", "Usuário", "Data de Emprestimo"]
}

for nome_arquivo, cabecalhos in arquivos.items():
    caminho = os.path.join("data", nome_arquivo)
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cabecalhos)
            writer.writeheader()

def carregar_dados(nome_arquivo):
    caminho = os.path.join("data", nome_arquivo)
    dados = []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linha in reader:
                dados.append(linha)
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
    return dados

def salvar_dados(nome_arquivo, dados, cabecalhos):
    caminho = os.path.join("data", nome_arquivo)
    try:
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cabecalhos)
            writer.writeheader()
            writer.writerows(dados)
        return True
    except Exception as e:
        print(f"Erro ao salvar o arquivo {nome_arquivo}: {e}")
        return False

