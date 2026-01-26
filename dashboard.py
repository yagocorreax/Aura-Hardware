import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG STREAMLIT
# =========================
st.set_page_config(page_title="Aura Hardware", layout="wide")

# =========================
# DARK THEME CORPORATIVO
# =========================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
div[data-testid="stMetric"] {
    background-color: #1f2937;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
h1, h2, h3, h4 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Aura Hardware")

# =========================
# CARREGAR DADOS
# =========================
fat = pd.read_csv("dados/limpo/faturamento_mensal.csv")
prod = pd.read_csv("dados/limpo/produtos_mais_vendidos.csv")
clientes = pd.read_csv("dados/limpo/clientes_limpos.csv")
pedidos = pd.read_csv("dados/limpo/pedidos_limpos.csv")

# =========================
# KPI CARDS
# =========================
faturamento_total = fat["valor_total"].sum()
total_produtos = prod["quantidade"].sum()
total_clientes = clientes["id"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
col2.metric("📦 Produtos Vendidos", f"{total_produtos:,}")
col3.metric("👥 Clientes", f"{total_clientes:,}")

st.divider()

# =========================
# FATURAMENTO MENSAL (MÊS POR EXTENSO)
# =========================
fat["ano_mes"] = pd.to_datetime(fat["ano_mes"])

meses_pt = {
    1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril",
    5:"Maio", 6:"Junho", 7:"Julho", 8:"Agosto",
    9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"
}

fat["mes"] = fat["ano_mes"].dt.month.map(meses_pt)
fat["ano"] = fat["ano_mes"].dt.year
fat["mes_ano"] = fat["mes"] + "/" + fat["ano"].astype(str)

st.subheader("📈 Faturamento Mensal")

fig_fat = px.line(
    fat,
    x="mes_ano",
    y="valor_total",
    title="Evolução do Faturamento"
)

fig_fat.update_layout(
    template="plotly_dark",
    xaxis_title="Mês/Ano",
    yaxis_title="Faturamento (R$)"
)

st.plotly_chart(fig_fat, use_container_width=True)

# =========================
# TOP 20 PRODUTOS MAIS VENDIDOS (VERMELHO)
# =========================
st.subheader("🔥 Top 20 Produtos Mais Vendidos")

prod = prod.rename(columns={"produto_id": "Id do Produto"})
top20 = prod.sort_values("quantidade", ascending=False).head(20)

fig_prod = px.bar(
    top20,
    x="Id do Produto",
    y="quantidade",
    title="Top 20 Produtos Mais Vendidos",
    color_discrete_sequence=["#ef4444"]  # VERMELHO CORPORATIVO
)

fig_prod.update_layout(
    template="plotly_dark",
    xaxis_title="Id do Produto",
    yaxis_title="Quantidade Vendida"
)

st.plotly_chart(fig_prod, use_container_width=True)

# =========================
# TOP 50 CLIENTES COM NOME (VERDE)
# =========================
st.subheader("🏆 Top 50 Clientes que Mais Compraram")

# Contar pedidos por cliente
clientes_top = pedidos.groupby("cliente_id")["valor_total"].count().reset_index()
clientes_top.columns = ["cliente_id", "quantidade_compras"]

# JOIN com clientes
clientes_top = clientes_top.merge(
    clientes[["id", "nome"]],
    left_on="cliente_id",
    right_on="id",
    how="left"
)

# Ordenar TOP 50
clientes_top = clientes_top.sort_values("quantidade_compras", ascending=False).head(50)

# Gráfico VERDE
fig_clientes = px.bar(
    clientes_top,
    x="nome",
    y="quantidade_compras",
    title="Top 50 Clientes por Quantidade de Compras",
    color_discrete_sequence=["#10b981"]  # VERDE CORPORATIVO
)

fig_clientes.update_layout(
    template="plotly_dark",
    xaxis_title="Cliente",
    yaxis_title="Quantidade de Compras"
)

st.plotly_chart(fig_clientes, use_container_width=True)







