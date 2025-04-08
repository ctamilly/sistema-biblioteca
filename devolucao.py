import streamlit as st
import pandas as pd
from datetime import datetime
from dados import carregar_dados, salvar_dados
from emprestimo import atualizar_emprestimo

ARQUIVOS_EMPRESTIMO = "emprestimos.csv"
ARQUIVO_USUARIOS = "usuarios.csv"
ARQUIVO_DEVOLUCAO = "devolucoes.csv"

def cadastrar_devolucao():
    st.subheader("Realizar emprestimos")
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)

    list_emprestimo = [emprestimo["Livro"] for emprestimo in emprestimos]

    nome_livro = st.selectbox("Livro para devolver", list_emprestimo)
    nome_usuario = ''
    data_hora = st.date_input("Data e Hora da devolução", value=datetime.now())
    
    for emprestimo in emprestimos:
        if emprestimo["Livro"] == nome_livro:
            nome_usuario = emprestimo["Usuario"]
            break
    st.success( nome_usuario)
    
    if st.button("Devolver"):
        devolucao = {
            "Livro": nome_livro,
            "Usuario": nome_usuario,
            "Data_Devolucao": data_hora
        }

        devolucoes = carregar_dados(ARQUIVO_DEVOLUCAO)
        devolucoes.append(devolucao)

        salvar_dados(ARQUIVO_DEVOLUCAO, devolucoes, ["Livro","Usuario","Data_Devolucao"])
        st.success("Devolução realizado com sucesso")
        apagar_emprestimo(nome_livro, nome_usuario)
        listar_devolucoes()

def listar_devolucoes():
    st.subheader("Devoluções Realizados")

    devolucoes = carregar_dados(ARQUIVO_DEVOLUCAO)

    if devolucoes:
        df_devolucoes = pd.DataFrame(devolucoes)
        st.table(df_devolucoes)
    else:
        st.info("Nenhuma devolução realizado.")

def apagar_emprestimo(nome_livro, nome):
    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)
    novos_emprestimos = [e for e in emprestimos if e["Livro"] != nome_livro]

    if len(novos_emprestimos) < len(emprestimos):
        salvar_dados(ARQUIVOS_EMPRESTIMO, novos_emprestimos, ["Livro","Usuario","Data_Emprestimo"])
        st.success(f"Emprestimo removido com sucesso.")
    else:
        st.warning("Emprestimo não encontrado.")
    
    atualizar_emprestimo(nome)