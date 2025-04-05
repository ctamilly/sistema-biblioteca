import streamlit as st
from livros import cadastrar_livro, listar_livros
from usuarios import cadastrar_usuario, listar_usuarios
from emprestimo import cadastrar_emprestimo, listar_emprestimos
from devolucao import cadastrar_devolucao

st.title("Sistema de Biblioteca")

menu = st.sidebar.radio("Menu", ["Cadastrar Livro", "Listar Livros", "Cadastrar Usuário", "Listar Usuários", "Realizar Emprestimos", "Mostrar Emprestimos", "Devolucoes"])

if menu == "Cadastrar Livro":
    cadastrar_livro()
elif menu == "Listar Livros":
    listar_livros()
elif menu == "Cadastrar Usuário":
    cadastrar_usuario()
elif menu == "Listar Usuários":
    listar_usuarios()
elif menu == "Realizar Emprestimos":
    cadastrar_emprestimo()
elif menu == "Mostrar Emprestimos":
    listar_emprestimos()
elif menu == "Devolucoes":
    cadastrar_devolucao()
