import sqlite3
import random
from faker import Faker

fake = Faker("pt-BR")

con = sqlite3.connect("Data/Raw/aura_hardware.db")
cursor = con.cursor()

cursor.execute("""
    DROP TABLE IF EXISTS clientes;
    DROP TABLE IF EXISTS produtos;
    DROP TABLE IF EXISTS categorias;
    DROP TABLE IF EXISTS pedidos;
    DROP TABLE IF EXISTS itens_pedido;       
""")

cursor.execute("""
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    descricao TEXT,
    data_cadastro TEXT );

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    telefone TEXT,
    cpf TEXT,
    data_nascimento TEXT,
    endereco TEXT,
    cidade TEXT,
    estado TEXT,
    cep TEXT,
    data_cadastro TEXT );

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER,
    nome TEXT,
    descricao TEXT,
    preco REAL, 
    estoque INTEGER, 
    data_cadastro TEXT);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    data_pedido TEXT,
    status TEXT,
    valor_total REAL);

CREATE_TABLE itens_pedido (
    )              




               """)