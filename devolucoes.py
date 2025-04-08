import streamlit as st
import pandas as pd
from datetime import datetime
from dados import carregar_dados, salvar_dados

ARQUIVOS_EMPRESTIMO = "emprestimos.csv"
ARQUIVO_USUARIOS = "usuarios.csv"
ARQUIVO_DEVOLUCAO = "devolucoes.csv"

def cadastrar_devolucao():
    st.subheader("📦 Realizar Devolução")
    st.markdown("---")

    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)

    list_emprestimo = [e["Livro"] for e in emprestimos]

    if not list_emprestimo:
        st.info("📭 Nenhum livro está emprestado atualmente.")
        return

    nome_livro = st.selectbox("📖 Livro para Devolver", list_emprestimo)
    nome_usuario = next((e["Usuario"] for e in emprestimos if e["Livro"] == nome_livro), "")

    if nome_usuario:
        st.markdown(f"👤 **Usuário:** {nome_usuario}")
    else:
        st.warning("⚠️ Usuário não encontrado.")
        return

    data_hora = st.date_input("📅 Data da Devolução", value=datetime.now())

    if st.button("Confirmar Devolução"):
        devolucao = {
            "Livro": nome_livro,
            "Usuario": nome_usuario,
            "Data_Devolucao": data_hora.strftime("%d-%m-%Y")
        }

        devolucoes = carregar_dados(ARQUIVO_DEVOLUCAO)
        devolucoes.append(devolucao)
        salvar_dados(ARQUIVO_DEVOLUCAO, devolucoes, ["Livro", "Usuario", "Data_Devolucao"])
        apagar_emprestimo(nome_livro, nome_usuario)

        st.success("✅ Devolução registrada com sucesso!")
        listar_devolucoes()

def listar_devolucoes():
    st.subheader("📋 Devoluções Realizadas")
    st.markdown("---")

    devolucoes = carregar_dados(ARQUIVO_DEVOLUCAO)

    if devolucoes:
        def obter_data_devolucao(item):
            return item["Data_Devolucao"]

        devolucoes.sort(key=obter_data_devolucao, reverse=True)
        df = pd.DataFrame(devolucoes)
        st.table(df)
    else:
        st.info("📭 Nenhuma devolução registrada ainda.")

def apagar_emprestimo(nome_livro, nome_usuario):
    emprestimos = carregar_dados(ARQUIVOS_EMPRESTIMO)
    novos_emprestimos = [e for e in emprestimos if e["Livro"] != nome_livro]

    if len(novos_emprestimos) < len(emprestimos):
        salvar_dados(ARQUIVOS_EMPRESTIMO, novos_emprestimos, ["Livro", "Usuario", "Data_Emprestimo"])
        remover_livro_emprestado(nome_usuario, nome_livro)
        st.success(f"📚 Empréstimo do livro '{nome_livro}' removido com sucesso.")
    else:
        st.warning("⚠️ Empréstimo não encontrado para remoção.")

def remover_livro_emprestado(nome_usuario, livro_removido):
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    for usuario in usuarios:
        if usuario["Nome"] == nome_usuario:
            livros = usuario.get("Livros_Emprestados", "")
            lista_livros = [livro.strip() for livro in livros.split(",") if livro.strip()]
            if livro_removido in lista_livros:
                lista_livros.remove(livro_removido)
            usuario["Livros_Emprestados"] = ", ".join(lista_livros)
            break

    salvar_dados(ARQUIVO_USUARIOS, usuarios, ["ID", "Nome", "Email", "Tipo", "Livros_Emprestados"])
