import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Aura Hardware", layout="wide")


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

fat = pd.read_csv("dados/limpo/faturamento_mensal.csv")
prod = pd.read_csv("dados/limpo/produtos_mais_vendidos.csv")
clientes = pd.read_csv("dados/limpo/clientes_limpos.csv")
pedidos = pd.read_csv("dados/limpo/pedidos_limpos.csv")


faturamento_total = fat["valor_total"].sum()
total_produtos = prod["quantidade"].sum()
total_clientes = clientes["id"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
col2.metric("📦 Produtos Vendidos", f"{total_produtos:,}")
col3.metric("👥 Clientes", f"{total_clientes:,}")

st.divider()

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

st.subheader("🔥 Top 20 Produtos Mais Vendidos")

prod = prod.rename(columns={"produto_id": "Id do Produto"})
top20 = prod.sort_values("quantidade", ascending=False).head(20)

fig_prod = px.bar(
    top20,
    x="Id do Produto",
    y="quantidade",
    title="Top 20 Produtos Mais Vendidos",
    color_discrete_sequence=["#ef4444"]  
)

fig_prod.update_layout(
    template="plotly_dark",
    xaxis_title="Id do Produto",
    yaxis_title="Quantidade Vendida"
)

st.plotly_chart(fig_prod, use_container_width=True)


st.subheader("🏆 Top 50 Clientes que Mais Compraram")


clientes_top = pedidos.groupby("cliente_id")["valor_total"].count().reset_index()
clientes_top.columns = ["cliente_id", "quantidade_compras"]

clientes_top = clientes_top.merge(
    clientes[["id", "nome"]],
    left_on="cliente_id",
    right_on="id",
    how="left"
)

clientes_top = clientes_top.sort_values("quantidade_compras", ascending=False).head(50)


fig_clientes = px.bar(
    clientes_top,
    x="nome",
    y="quantidade_compras",
    title="Top 50 Clientes por Quantidade de Compras",
    color_discrete_sequence=["#10b981"]  
)

fig_clientes.update_layout(
    template="plotly_dark",
    xaxis_title="Cliente",
    yaxis_title="Quantidade de Compras"
)

st.plotly_chart(fig_clientes, use_container_width=True)

st.subheader("📋 Segmentação de Clientes")

clientes_segmentados = clientes.copy()
clientes_segmentados.columns = [c.lower().strip() for c in clientes_segmentados.columns]


def padronizar_telefone(tel):
    if pd.isna(tel):
        return None

    tel = ''.join(filter(str.isdigit, str(tel)))

    if len(tel) > 13:
        tel = tel[-13:]

    # Detectar país
    if len(tel) == 13:  # ex: 5511987654321
        pais = tel[:2]
        ddd = tel[2:4]
        numero = tel[4:]
    elif len(tel) == 12:  # ex: 551987654321 (sem DDD separado)
        pais = tel[:2]
        ddd = tel[2:4]
        numero = tel[4:]
    elif len(tel) == 11:  # Brasil sem código país
        pais = "55"
        ddd = tel[:2]
        numero = tel[2:]
    elif len(tel) == 10:  # fixo sem país
        pais = "55"
        ddd = tel[:2]
        numero = tel[2:]
    else:
        return tel  

    if len(numero) == 9:
        return f"+{pais} ({ddd}) {numero[:5]}-{numero[5:]}"
   
    elif len(numero) == 8:
        return f"+{pais} ({ddd}) {numero[:4]}-{numero[4:]}"
    
    return f"+{pais} ({ddd}) {numero}"

for col in clientes_segmentados.columns:
    if "telefone" in col.lower() or "phone" in col.lower() or "tel" in col.lower():
        clientes_segmentados[col] = clientes_segmentados[col].apply(padronizar_telefone)

st.dataframe(
    clientes_segmentados,
    use_container_width=True,
    height=400
)








