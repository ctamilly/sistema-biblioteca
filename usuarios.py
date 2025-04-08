import streamlit as st
import uuid
import pandas as pd
from dados import carregar_dados, salvar_dados

ARQUIVO_USUARIOS = "usuarios.csv"

def cadastrar_usuario():
    st.subheader("📝 Cadastro de Usuário")
    st.markdown("---")

    nome = st.text_input("👤 Nome do Usuário")
    email = st.text_input("📧 E-mail")
    tipo = st.selectbox("📘 Tipo de Usuário", ["Aluno", "Professor", "Visitante"])

    if st.button("Cadastrar Usuário"):
        if not nome.strip() or not email.strip() or not tipo.strip():
            st.warning("⚠️ Por favor, preencha todos os campos obrigatórios: Nome, E-mail e Tipo.")
            return

        usuarios = carregar_dados(ARQUIVO_USUARIOS)
        emails_existentes = set(u["Email"].strip().lower() for u in usuarios)

        if email.strip().lower() in emails_existentes:
            st.error("⚠️ Este e-mail já está cadastrado. Tente outro.")
            return

        usuario = {
            "ID": str(uuid.uuid4())[:6],
            "Nome": nome.strip(),
            "Email": email.strip(),
            "Tipo": tipo,
            "Livros_Emprestados": ""
        }

        usuarios.append(usuario)

        sucesso = salvar_dados(ARQUIVO_USUARIOS, usuarios, ["ID", "Nome", "Email", "Tipo", "Livros_Emprestados"])
        if sucesso:
            st.success(f"✅ Usuário '{nome}' cadastrado com sucesso!")

def listar_usuarios():
    st.subheader("👥 Usuários Cadastrados")
    st.markdown("---")

    usuarios = carregar_dados(ARQUIVO_USUARIOS)

    if not usuarios:
        st.info("📭 Nenhum usuário cadastrado.")
        return

    busca = st.text_input("🔍 Buscar por nome")

    if busca:
        usuarios = [u for u in usuarios if busca.lower() in u["Nome"].lower()]

    for u in usuarios:
        livros = u.get("Livros_Emprestados", "")
        u["Livros Emprestados"] = livros if livros else "Nenhum"

    usuarios.sort(key=lambda u: u["Nome"])
    df = pd.DataFrame(usuarios)[["ID", "Nome", "Email", "Tipo", "Livros Emprestados"]]
    st.table(df)

