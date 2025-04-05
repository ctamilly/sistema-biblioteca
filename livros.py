import streamlit as st
import pandas as pd
from dados import carregar_dados, salvar_dados

ARQUIVO_LIVROS = "livros.csv"
CAMPOS = ["Título", "Autor", "Ano", "ISBN", "Categoria"]

def cadastrar_livro():
    st.subheader("📘 Cadastro de Livro")

    titulo = st.text_input("Título do Livro")
    autor = st.text_input("Autor")
    ano = st.number_input("Ano de Publicação", min_value=1900, max_value=2100, step=1)
    isbn = st.text_input("ISBN")
    categoria = st.selectbox("Categoria", ["Computação", "Biologia", "Matemática", "Economia", "História"])

    if st.button("Cadastrar Livro"):
        if titulo and autor and isbn:
            novo_livro = {
                "Título": titulo,
                "Autor": autor,
                "Ano": ano,
                "ISBN": isbn,
                "Categoria": categoria
            }

            livros = carregar_dados(ARQUIVO_LIVROS)
            livros.append(novo_livro)
            salvar_dados(ARQUIVO_LIVROS, livros, CAMPOS)

            st.success(f"Livro '{titulo}' cadastrado com sucesso!")
        else:
            st.warning("Por favor, preencha todos os campos obrigatórios.")

def listar_livros():
    st.subheader("📚 Livros Cadastrados")

    livros = carregar_dados(ARQUIVO_LIVROS)

    if livros:
        df_livros = pd.DataFrame(livros)
        st.table(df_livros)
    else:
        st.info("Nenhum livro cadastrado.")

