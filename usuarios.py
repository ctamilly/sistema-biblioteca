import streamlit as st
import uuid
import pandas as pd
from dados import carregar_dados, salvar_dados

ARQUIVO_USUARIOS = "usuarios.csv"

def cadastrar_usuario():
    st.subheader("Cadastro de Usuário")

    nome = st.text_input("Nome do Usuário")
    email = st.text_input("E-mail")
    tipo = st.selectbox("Tipo de Usuário", ["Aluno", "Professor", "Visitante"])

    if st.button("Cadastrar"):
        usuario = {
            "ID": str(uuid.uuid4()),
            "Nome": nome,
            "Email": email,
            "Tipo": tipo,
            "Livros_Emprestados": ""  # Campo vazio no início
        }

        usuarios = carregar_dados(ARQUIVO_USUARIOS)
        usuarios.append(usuario)

        salvar_dados(ARQUIVO_USUARIOS, usuarios, ["ID", "Nome", "Email", "Tipo", "Livros_Emprestados"])
        st.success(f"Usuário '{nome}' cadastrado com sucesso!")

def listar_usuarios():
    st.subheader("👥 Usuários Cadastrados")

    usuarios = carregar_dados(ARQUIVO_USUARIOS)

    if usuarios:
        # Se o campo Livros_Emprestados for string separada por vírgula, formatamos para lista legível
        for u in usuarios:
            emprestados = u.get("Livros_Emprestados", "")
            u["Livros Emprestados"] = emprestados if emprestados else "Nenhum"

        df_usuarios = pd.DataFrame(usuarios)[["ID", "Nome", "Email", "Tipo", "Livros Emprestados"]]
        st.table(df_usuarios)
    else:
        st.info("Nenhum usuário cadastrado.")


