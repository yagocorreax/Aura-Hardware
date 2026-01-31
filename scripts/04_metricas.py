import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import PASTA_DADOS_LIMPO

os.makedirs(PASTA_DADOS_LIMPO, exist_ok=True)

df_clientes = pd.read_csv(f"{PASTA_DADOS_LIMPO}/clientes_limpos.csv", encoding="utf-8-sig")
df_produtos = pd.read_csv(f"{PASTA_DADOS_LIMPO}/produtos_limpos.csv", encoding="utf-8-sig")
df_pedidos = pd.read_csv(f"{PASTA_DADOS_LIMPO}/pedidos_limpos.csv", encoding="utf-8-sig")
df_itens = pd.read_csv(f"{PASTA_DADOS_LIMPO}/itens_pedido_limpos.csv", encoding="utf-8-sig")
df_categorias = pd.read_csv(f"{PASTA_DADOS_LIMPO}/categoria_produtos_limpos.csv", encoding="utf-8-sig")

df_pedidos["data_pedido"] = pd.to_datetime(df_pedidos["data_pedido"], errors="coerce")
df_clientes["data_nascimento"] = pd.to_datetime(df_clientes["data_nascimento"], errors="coerce")

df_faturamento = df_pedidos.copy()
df_faturamento["ano_mes"] = df_faturamento["data_pedido"].dt.to_period("M")
faturamento_mensal = df_faturamento.groupby("ano_mes")["valor_total"].sum().reset_index()
faturamento_mensal.to_csv(f"{PASTA_DADOS_LIMPO}/faturamento_mensal.csv", index=False, encoding="utf-8-sig")

ticket_medio = df_pedidos.groupby("cliente_id")["valor_total"].mean().reset_index()
ticket_medio = ticket_medio.merge(df_clientes[["id", "nome"]], left_on="cliente_id", right_on="id", how="left")
ticket_medio = ticket_medio[["cliente_id", "nome", "valor_total"]].rename(columns={"valor_total": "ticket_medio"})
ticket_medio.to_csv(f"{PASTA_DADOS_LIMPO}/ticket_medio_cliente.csv", index=False, encoding="utf-8-sig")

produtos_vendas = df_itens.groupby("produto_id")["quantidade"].sum().reset_index()
produtos_vendas = produtos_vendas.merge(df_produtos[["id", "nome"]], left_on="produto_id", right_on="id", how="left")
produtos_vendas = produtos_vendas[["produto_id", "nome", "quantidade"]].sort_values("quantidade", ascending=False)
produtos_vendas.to_csv(f"{PASTA_DADOS_LIMPO}/produtos_mais_vendidos.csv", index=False, encoding="utf-8-sig")

df_clientes["idade"] = (pd.to_datetime("today") - df_clientes["data_nascimento"]).dt.days // 365
df_clientes_segmentados = df_clientes[["id", "nome", "idade", "genero", "cidade", "estado"]]
df_clientes_segmentados.to_csv(f"{PASTA_DADOS_LIMPO}/clientes_segmentados.csv", index=False, encoding="utf-8-sig")

estoque_alerta = df_produtos[df_produtos["estoque"] <= 10][["id", "nome", "estoque"]]
estoque_alerta.to_csv(f"{PASTA_DADOS_LIMPO}/estoque_alerta.csv", index=False, encoding="utf-8-sig")

print("MÉTRICAS GERADAS E SALVAS EM dados/limpo")
