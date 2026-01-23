import sqlite3
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import PASTA_DADOS_BRUTO

PASTA_DADOS = os.path.dirname(PASTA_DADOS_BRUTO)
os.makedirs(PASTA_DADOS, exist_ok=True)

db_path = os.path.join(PASTA_DADOS, "Aura_Hardware.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS categoria_produtos (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT,
    data_cadastro TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT,
    cpf TEXT,
    data_nascimento TEXT,
    endereco TEXT,
    cidade TEXT,
    estado TEXT,
    cep TEXT,
    data_cadastro TEXT,
    genero TEXT)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY,
    categoria_id INTEGER,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL,
    estoque INTEGER,
    data_cadastro TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categoria_produtos(id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER,
    data_pedido TEXT,
    status TEXT,
    valor_total REAL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id))
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER,
    produto_id INTEGER,
    quantidade INTEGER,
    valor_unitario REAL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id))
""")

conn.commit()

def carregar_csv_para_sqlite(nome_csv, nome_tabela):
    df = pd.read_csv(os.path.join(PASTA_DADOS_BRUTO, nome_csv))
    df.to_sql(nome_tabela, conn, if_exists='replace', index=False)
    print(f"Tabela {nome_tabela} populada com sucesso")

carregar_csv_para_sqlite("categoria_produtos.csv", "categoria_produtos")
carregar_csv_para_sqlite("clientes.csv", "clientes")
carregar_csv_para_sqlite("produtos.csv", "produtos")
carregar_csv_para_sqlite("pedidos.csv", "pedidos")
carregar_csv_para_sqlite("itens_pedido.csv", "itens_pedido")

conn.close()
print(f"Banco SQLite criado em {db_path}")
