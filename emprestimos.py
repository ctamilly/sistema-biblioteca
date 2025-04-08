import streamlit as st
import pandas as pd
from datetime import datetime
from dados import carregar_dados, salvar_dados

ARQUIVOS_EMPRESTIMO = "emprestimos.csv"
ARQUIVO_USUARIOS = "usuarios.csv"
ARQUIVO_LIVROS = "livros.csv"

def cadastrar_emprestimo():
    st.subheader("📚 Realizar Empréstimo")
    st.markdown("---")

    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    livros = carregar_dados(ARQUIVO_LIVROS)
    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)

    list_usuario = [usuario["Nome"] for usuario in usuarios]
    list_emprestimo = {emprestimo ["Livro"] for emprestimo in emprestimos}
    list_livros_disponiveis = [livro["Título"] for livro in livros if livro["Título"] not in list_emprestimo]   

    if not list_livros_disponiveis:
        st.info("📭 Nenhum livro disponível para empréstimo no momento.")
        return

    nome = st.selectbox("👤 Nome do Usuário", list_usuario)
    nome_livro = st.selectbox("📖 Nome do Livro", list_livros_disponiveis)

    data_hora = st.date_input("📅 Data do Empréstimo", value=datetime.now())

    if st.button("Confirmar Empréstimo"):
        if nome and nome_livro:
            novo_emprestimo = {
                "Livro": nome_livro,
                "Usuario": nome,
                "Data_Emprestimo": data_hora.strftime("%d-%m-%Y")
            }

            emprestimos.append(novo_emprestimo)
            salvar_dados(ARQUIVOS_EMPRESTIMO, emprestimos, ["Livro", "Usuario", "Data_Emprestimo"])

            atualizar_emprestimo(nome, nome_livro)
            st.success(f"✅ Empréstimo de '{nome_livro}' para '{nome}' registrado com sucesso!")
        else:
            st.warning("⚠️ Preencha todos os campos antes de confirmar.")

def listar_emprestimos():
    st.subheader("📋 Empréstimos Ativos")
    st.markdown("---")

    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)

    if emprestimos:
        def obter_usuario(emprestimo):
            return emprestimo["Usuario"]

        emprestimos.sort(key=obter_usuario)
        df = pd.DataFrame(emprestimos)
        st.table(df)
    else:
        st.info("📭 Nenhum empréstimo ativo.")

def atualizar_emprestimo(nome, novo_livro=""):
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    atualizado = False

    for usuario in usuarios:
        if usuario["Nome"] == nome:
            livros = usuario.get("Livros_Emprestados", "")
            lista_livros = [livro.strip() for livro in livros.split(",") if livro.strip()]
            if novo_livro and novo_livro not in lista_livros:
                lista_livros.append(novo_livro)
            usuario["Livros_Emprestados"] = ", ".join(lista_livros)
            atualizado = True
            break

    if atualizado:
        salvar_dados(ARQUIVO_USUARIOS, usuarios, ["ID", "Nome", "Email", "Tipo", "Livros_Emprestados"])
    else:
        st.error("❌ Usuário não encontrado para atualizar empréstimo.")
