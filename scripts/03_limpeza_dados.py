import sqlite3
import pandas as pd
import re
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import PASTA_DADOS_LIMPO
from config.config import PASTA_DADOS_BRUTO

os.makedirs(PASTA_DADOS_LIMPO, exist_ok=True)

db_path = os.path.join(os.path.dirname(PASTA_DADOS_BRUTO), "Aura_Hardware.db")
conn = sqlite3.connect(db_path)

def limpar_clientes(df):
    df = df.drop_duplicates(subset="cpf")
    df["nome"] = df["nome"].str.strip()
    df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], errors="coerce")
    df = df[df["data_nascimento"] <= pd.to_datetime("today") - pd.DateOffset(years=18)]
    df["data_cadastro"] = pd.to_datetime(df["data_cadastro"], errors="coerce")
    regex_email = r"^[\w\.-]+@(gmail|hotmail)\.com$"
    df["email"] = df["email"].apply(lambda x: x if isinstance(x,str) and re.match(regex_email,x) else None)
    df["cep"] = df["cep"].astype(str).str.replace("-", "").str[:8]
    df["cpf"] = df["cpf"].astype(str)
    return df

def limpar_produtos(df):
    df["nome"] = df["nome"].str.strip()
    df["descricao"] = df["descricao"].str.strip()
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce").fillna(0)
    df["estoque"] = pd.to_numeric(df["estoque"], errors="coerce").fillna(0)
    df["data_cadastro"] = pd.to_datetime(df["data_cadastro"], errors="coerce")
    return df

def limpar_categorias(df):
    df["nome"] = df["nome"].str.strip()
    df["descricao"] = df["descricao"].str.strip()
    df["data_cadastro"] = pd.to_datetime(df["data_cadastro"], errors="coerce")
    return df

def limpar_pedidos(df):
    df["data_pedido"] = pd.to_datetime(df["data_pedido"], errors="coerce")
    df["status"] = df["status"].fillna("Pendente")
    df["valor_total"] = pd.to_numeric(df["valor_total"], errors="coerce").fillna(0)
    return df

def limpar_itens(df):
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(0)
    df["valor_unitario"] = pd.to_numeric(df["valor_unitario"], errors="coerce").fillna(0)
    return df

df_clientes = limpar_clientes(pd.read_sql("SELECT * FROM clientes", conn))
df_produtos = limpar_produtos(pd.read_sql("SELECT * FROM produtos", conn))
df_categorias = limpar_categorias(pd.read_sql("SELECT * FROM categoria_produtos", conn))
df_pedidos = limpar_pedidos(pd.read_sql("SELECT * FROM pedidos", conn))
df_itens = limpar_itens(pd.read_sql("SELECT * FROM itens_pedido", conn))

df_clientes.to_csv(f"{PASTA_DADOS_LIMPO}/clientes_limpos.csv", index=False, encoding="utf-8-sig")
df_produtos.to_csv(f"{PASTA_DADOS_LIMPO}/produtos_limpos.csv", index=False, encoding="utf-8-sig")
df_categorias.to_csv(f"{PASTA_DADOS_LIMPO}/categoria_produtos_limpos.csv", index=False, encoding="utf-8-sig")
df_pedidos.to_csv(f"{PASTA_DADOS_LIMPO}/pedidos_limpos.csv", index=False, encoding="utf-8-sig")
df_itens.to_csv(f"{PASTA_DADOS_LIMPO}/itens_pedido_limpos.csv", index=False, encoding="utf-8-sig")

conn.close()
print("DADOS LIMPOS SALVOS EM dados/limpo")


