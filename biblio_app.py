import streamlit as st
from livros import cadastrar_livro, listar_livros
from usuarios import cadastrar_usuario, listar_usuarios
from emprestimos import cadastrar_emprestimo, listar_emprestimos
from devolucoes import cadastrar_devolucao
from relatorios import mostrar_estatisticas

st.set_page_config(page_title="Sistema de Biblioteca", layout="wide")
st.title("Sistema de Biblioteca")

secao = st.sidebar.selectbox("📂 Seções", ["Cadastros", "Empréstimos e Devoluções", "Listas e Buscas", "Relatórios"])

if secao == "Cadastros":
    submenu = st.sidebar.radio(" ", ["Cadastrar Usuário", "Cadastrar Livro"])
    if submenu == "Cadastrar Usuário":
        cadastrar_usuario()
    elif submenu == "Cadastrar Livro":
        cadastrar_livro()
    
elif secao == "Empréstimos e Devoluções":
    submenu = st.sidebar.radio(" ", ["Realizar Empréstimo", "Registrar Devolução"])
    if submenu == "Realizar Empréstimo":
        cadastrar_emprestimo()
    elif submenu == "Registrar Devolução":
        cadastrar_devolucao()
        
elif secao == "Listas e Buscas":
    submenu = st.sidebar.radio(" ", ["Listar Livros", "Listar Usuários", "Listar Empréstimos"])
    if submenu == "Listar Livros":
        listar_livros()
    elif submenu == "Listar Usuários":
        listar_usuarios()
    elif submenu == "Listar Empréstimos":
        listar_emprestimos()
        
elif secao == "Relatórios":
    mostrar_estatisticas()
