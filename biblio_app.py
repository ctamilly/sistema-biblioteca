import streamlit as st
from livros import cadastrar_livro, listar_livros
from usuarios import cadastrar_usuario, listar_usuarios

st.title("Sistema de Biblioteca")

menu = st.sidebar.radio("Menu", ["Cadastrar Livro", "Listar Livros", "Cadastrar Usuário", "Listar Usuários"])

if menu == "Cadastrar Livro":
    cadastrar_livro()
elif menu == "Listar Livros":
    listar_livros()
elif menu == "Cadastrar Usuário":
    cadastrar_usuario()
elif menu == "Listar Usuários":
    listar_usuarios()
