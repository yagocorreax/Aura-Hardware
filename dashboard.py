import pandas as pd
import streamlit as st
import os
import plotly.express as px

# ================= CONFIG =================
st.set_page_config(page_title="Aura Hardware", layout="wide")

PASTA = "dados/limpo"

# ================= FUNÇÃO AUTO COLUNA =================
def achar_coluna(df, palavras):
    for col in df.columns:
        for p in palavras:
            if p.lower() in col.lower():
                return col
    return None

# ================= CARREGAR DADOS =================
fat = pd.read_csv(os.path.join(PASTA, "faturamento_mensal.csv"))
prod = pd.read_csv(os.path.join(PASTA, "produtos_mais_vendidos.csv"))
seg = pd.read_csv(os.path.join(PASTA, "clientes_segmentados.csv"))

# ================= DETECTAR COLUNAS =================
col_data = achar_coluna(fat, ["mes", "data", "ano"])
col_fat = achar_coluna(fat, ["faturamento", "valor", "total"])

col_prod_nome = achar_coluna(prod, ["produto", "nome"])
col_prod_qtd = achar_coluna(prod, ["quantidade", "qtd", "vendida"])

col_seg = achar_coluna(seg, ["segmento", "classe"])

# ================= DASHBOARD =================
st.title("📊 Aura Hardware")

# KPIs
faturamento_total = fat[col_fat].sum()
qtd_clientes = len(seg)
ticket_medio = faturamento_total / qtd_clientes

col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
col2.metric("👥 Total de Clientes", qtd_clientes)
col3.metric("🧾 Ticket Médio", f"R$ {ticket_medio:,.2f}")

# ================= GRÁFICO FATURAMENTO =================
st.subheader("📈 Faturamento Mensal")

fig_fat = px.line(fat, x=col_data, y=col_fat, title="Evolução do Faturamento")
st.plotly_chart(fig_fat, use_container_width=True)

# ================= PRODUTOS MAIS VENDIDOS =================
st.subheader("🔥 Produtos Mais Vendidos")

fig_prod = px.bar(prod, x=col_prod_qtd, y=col_prod_nome, orientation="h")
st.plotly_chart(fig_prod, use_container_width=True)

# ================= SEGMENTAÇÃO CLIENTES =================
st.subheader("👤 Segmentação de Clientes")

seg_count = seg[col_seg].value_counts().reset_index()
seg_count.columns = ["Segmento", "Quantidade"]

fig_seg = px.pie(seg_count, names="Segmento", values="Quantidade")
st.plotly_chart(fig_seg, use_container_width=True)

# ================= TABELAS =================
st.subheader("📋 Dados Brutos")
st.dataframe(fat)

