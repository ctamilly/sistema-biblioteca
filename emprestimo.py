import streamlit as st
import pandas as pd
from datetime import datetime
from dados import carregar_dados, salvar_dados

ARQUIVOS_EMPRESTIMO = "emprestimos.csv"
ARQUIVO_USUARIOS = "usuarios.csv"
ARQUIVO_LIVROS = "livros.csv"

def cadastrar_emprestimo():
    st.subheader("Realizar emprestimos")
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    livros = carregar_dados(ARQUIVO_LIVROS)
    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)

    list_usuario = [usuario["Nome"] for usuario in usuarios]
    list_livros = [livro["Título"] for livro in livros]
    list_emprestimo = [emprestimo["Livro"] for emprestimo in emprestimos]

    nome = st.selectbox("Nome do Usuário", list_usuario)
    nome_livro = st.selectbox("Nome do Livro", list_livros)
    data_hora = st.date_input("Data e Hora do empréstimo", value=datetime.now())

    if nome_livro in list_emprestimo:
        st.info(f"Esse livro já está sendo emprestado ")
        
    else:
        if st.button("Cadastrar"):
            emprestimo = {
                "Livro": nome_livro,
                "Usuario": nome,
                "Data_Emprestimo": data_hora
            }
            atualizar_emprestimo(nome, nome_livro)

            emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)
            emprestimos.append(emprestimo)

            salvar_dados(ARQUIVOS_EMPRESTIMO, emprestimos, ["Livro","Usuario","Data_Emprestimo"])
            st.success(f"Emprestimo realizado com sucesso")

def listar_emprestimos():
    st.subheader("Emprestimos Realizados")

    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)

    if emprestimos:
        df_emprestimos = pd.DataFrame(emprestimos)
        st.table(df_emprestimos)
    else:
        st.info("Nenhum emprestimo Realizado.")

def atualizar_emprestimo(nome, livro_alvo = ""):
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    atualizado = False

    for usuario in usuarios:
        if usuario["Nome"] == nome:
            usuario["Livros_Emprestados"] = livro_alvo
            atualizado = True
            break

    if atualizado:
        salvar_dados(ARQUIVO_USUARIOS, usuarios, ["ID", "Nome", "Email", "Tipo", "Livros_Emprestados"])
        st.success(f"Empréstimo atualizado com sucesso!")
    else:
        st.error("Livro não encontrado nos empréstimos.")
