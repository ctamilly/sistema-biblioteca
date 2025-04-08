import streamlit as st
import pandas as pd
from dados import carregar_dados, salvar_dados

ARQUIVO_LIVROS = "livros.csv"
CAMPOS = ["Título", "Autor", "Ano", "ISBN", "Categoria"]

def cadastrar_livro():
    st.subheader("📘 Cadastro de Livro")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        titulo = st.text_input("📖 Título do Livro")
        autor = st.text_input("✍️ Autor")
        ano = st.number_input("📅 Ano de Publicação", min_value=0, step=1)

    with col2:
        isbn = st.text_input("🔢 ISBN")
        categoria = st.selectbox(
            "🏷️ Categoria",
            [
                "Ficção", "Romance", "Terror", "Mistério", "Fantasia",
                "Filosofia", "Suspense", "Biografia", "Drama", "Autoajuda",
                "Negócios", "Finanças", "História", "Ciência", "Estratégia"
            ]
        )

    if st.button("📥 Cadastrar Livro"):
        if titulo and autor and isbn:
            livros = carregar_dados(ARQUIVO_LIVROS)

            novo_livro = {
                "Título": titulo,
                "Autor": autor,
                "Ano": ano,
                "ISBN": isbn,
                "Categoria": categoria
            }

            livros.append(novo_livro)
            salvar_dados(ARQUIVO_LIVROS, livros, CAMPOS)

            st.success(f"✅ Livro '{titulo}' cadastrado com sucesso!")
        else:
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios: Título, Autor e ISBN.")

def listar_livros():
    st.subheader("📚 Livros Cadastrados")
    st.markdown("---")

    livros = carregar_dados(ARQUIVO_LIVROS)

    if not livros:
        st.info("📭 Nenhum livro cadastrado.")
        return

    filtro = st.radio("🔍 Buscar por", ["Todos", "Título", "Autor", "Categoria"])
    termo = ""

    if filtro == "Categoria":
        categorias_existentes = sorted(set(livro["Categoria"] for livro in livros))
        termo = st.selectbox("🏷️ Selecione a Categoria", categorias_existentes)
    elif filtro != "Todos":
        termo = st.text_input(f"Digite o {filtro} para buscar:")

    if filtro == "Todos":
        livros_filtrados = livros
    else:
        livros_filtrados = []
        for livro in livros:
            if termo.lower() in livro[filtro].lower():
                livros_filtrados.append(livro)

    if livros_filtrados:
        
        ordenacao = st.selectbox("📊 Ordenar por", ["Título (A-Z)", "Autor (A-Z)", "Ano (mais recente primeiro)"])

        def ordenar_por_titulo(livro):
            return livro["Título"]

        def ordenar_por_autor(livro):
            return livro["Autor"]

        def ordenar_por_ano(livro):
            return livro["Ano"]

        if ordenacao == "Título (A-Z)":
            livros_filtrados.sort(key=ordenar_por_titulo)
        elif ordenacao == "Autor (A-Z)":
            livros_filtrados.sort(key=ordenar_por_autor)
        elif ordenacao == "Ano (mais recente primeiro)":
            livros_filtrados.sort(key=ordenar_por_ano, reverse=True)

        df_livros = pd.DataFrame(livros_filtrados)
        st.table(df_livros)
    else:
        st.warning("❌ Nenhum livro encontrado com esse critério.")
