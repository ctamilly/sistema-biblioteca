import streamlit as st
import pandas as pd
from collections import Counter
from dados import carregar_dados
import plotly.express as px


ARQUIVO_LIVROS = "livros.csv"
ARQUIVO_USUARIOS = "usuarios.csv"
ARQUIVO_EMPRESTIMOS = "emprestimos.csv"

def mostrar_estatisticas():
    st.subheader("📊 Estatísticas e Relatórios")
    st.markdown("---")

    livros = carregar_dados(ARQUIVO_LIVROS)
    usuarios = carregar_dados(ARQUIVO_USUARIOS)
    emprestimos = carregar_dados(ARQUIVO_EMPRESTIMOS)

    st.markdown("### 📚 Quantidade de Livros por Categoria")

    if livros:
        categorias = {}

        for livro in livros:
            lista_categorias = set(map(str.strip, livro["Categoria"].split(",")))
            for cat in lista_categorias:
                categorias[cat] = categorias.get(cat, 0) + 1

        df_categorias = pd.DataFrame(list(categorias.items()), columns=["Categoria", "Quantidade"])
        st.bar_chart(df_categorias.set_index("Categoria"))
    else:
        st.info("Nenhum livro cadastrado para gerar estatísticas de categoria.")

    st.markdown("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔝 Livros Mais Emprestados")

        if emprestimos:
            contador_livros = Counter([e["Livro"] for e in emprestimos])
            mais_emprestados = contador_livros.most_common(5)

            df_mais = pd.DataFrame(mais_emprestados, columns=["Título", "Empréstimos"])
            st.table(df_mais)
        else:
            st.info("Nenhum empréstimo foi realizado até o momento.")

    with col2:
        st.markdown("### 👥 Empréstimos por Tipo de Usuário")

        if emprestimos and usuarios:
            tipo_por_usuario = {u["Nome"]: u["Tipo"] for u in usuarios}
            emprestimos_por_tipo = {}

            for emp in emprestimos:
                nome = emp.get("Usuário") or emp.get("Usuario")
                tipo = tipo_por_usuario.get(nome, "Desconhecido")
                emprestimos_por_tipo[tipo] = emprestimos_por_tipo.get(tipo, 0) + 1

            df_tipos = pd.DataFrame(list(emprestimos_por_tipo.items()), columns=["Tipo de Usuário", "Empréstimos"])
            st.plotly_chart(
                {
                    "data": [{
                        "type": "pie",
                        "labels": df_tipos["Tipo de Usuário"],
                        "values": df_tipos["Empréstimos"],
                        "hole": 0.3
                    }],
                },
                use_container_width=True
            )
        else:
            st.info("Não há dados suficientes para mostrar estatísticas por tipo de usuário.")
