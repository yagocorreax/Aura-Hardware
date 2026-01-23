import pandas as pd
import numpy as np
import random
from faker import Faker
import os
import sys

# ----------------- CORREÇÃO PARA WINDOWS / PATH -----------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import PASTA_DADOS_BRUTO

fake = Faker("pt_BR")
os.makedirs(PASTA_DADOS_BRUTO, exist_ok=True)

# ================== CATEGORIAS ==================
categorias = ["Processadores", "Placas de Vídeo", "Memórias RAM", "Armazenamento", "Placas-Mãe", "Fontes", "Gabinetes"]
descricoes_categorias = [
    "Componentes de alta performance para computadores modernos",
    "Produtos confiáveis e testados para uso diário e profissional",
    "Equipamentos que garantem estabilidade e velocidade",
    "Componentes essenciais para montagem de PCs completos",
    "Itens de qualidade para melhorar a experiência de hardware",
    "Produtos duráveis e eficientes para todas as tarefas",
    "Componentes com ótimo custo-benefício e garantia"
]

df_categorias = pd.DataFrame({
    "id": range(1, len(categorias)+1),
    "nome": categorias,
    "descricao": descricoes_categorias,
    "data_cadastro": [fake.date_this_decade() for _ in categorias]
})

df_categorias.to_csv(f"{PASTA_DADOS_BRUTO}/categoria_produtos.csv", index=False, encoding="utf-8-sig")

# ================== CLIENTES ==================
clientes = []

for i in range(3000):
    nome = fake.name()
    
    # Emails sujos (somente gmail/hotmail)
    if random.random() < 0.2:
        email = None
    else:
        dominio = random.choice(["gmail.com", "hotmail.com"])
        email = nome.replace(" ", "").lower() + str(random.randint(1,999)) + "@" + dominio
    
    # Inserir sujeira em nomes
    if random.random() < 0.1:
        nome = nome + "  "
    
    cliente = {
        "id": i+1,
        "nome": nome,
        "email": email,
        "telefone": fake.phone_number(),
        "cpf": fake.cpf(),
        "data_nascimento": fake.date_of_birth(minimum_age=16, maximum_age=80),
        "endereco": fake.address().replace("\n", " "),
        "cidade": fake.city(),
        "estado": fake.state_abbr(),
        "cep": fake.postcode().replace("-", "") if random.random() > 0.1 else fake.postcode() + "-",
        "data_cadastro": fake.date_this_decade(),
        "genero": random.choice(["Masculino", "Feminino", None])
    }
    
    clientes.append(cliente)

df_clientes = pd.DataFrame(clientes)

# Duplicar alguns clientes (erro real)
df_clientes = pd.concat([df_clientes, df_clientes.sample(50)])
df_clientes.to_csv(f"{PASTA_DADOS_BRUTO}/clientes.csv", index=False, encoding="utf-8-sig")

# ================== PRODUTOS ==================
descricoes_produtos = [
    "Placa de vídeo potente para jogos e edição de vídeo",
    "Processador rápido para multitarefas e softwares pesados",
    "Memória RAM de alta velocidade, ideal para overclock",
    "HD de grande capacidade para armazenamento de dados",
    "SSD rápido e confiável para uso diário e profissional",
    "Gabinete compacto com excelente ventilação",
    "Fonte de alimentação eficiente e silenciosa",
    "Placa-mãe com suporte para várias conexões e memória"
]

produtos = []
for i in range(500):
    produto = {
        "id": i+1,
        "categoria_id": random.randint(1, len(categorias)),
        "nome": f"Produto Hardware {i+1}",
        "descricao": random.choice(descricoes_produtos),
        "preco": round(random.uniform(50, 5000), 2),
        "estoque": random.randint(-10, 500),  # estoque negativo proposital
        "data_cadastro": fake.date_this_decade()
    }
    produtos.append(produto)

df_produtos = pd.DataFrame(produtos)
df_produtos.to_csv(f"{PASTA_DADOS_BRUTO}/produtos.csv", index=False, encoding="utf-8-sig")

# ================== PEDIDOS ==================
pedidos = []
for i in range(8000):
    pedido = {
        "id": i+1,
        "cliente_id": random.randint(1, 3000),
        "data_pedido": fake.date_between(start_date="-4y", end_date="today"),
        "status": random.choice(["Entregue", "Cancelado", "Pendente", None]),
        "valor_total": round(random.uniform(100, 15000), 2)
    }
    pedidos.append(pedido)

df_pedidos = pd.DataFrame(pedidos)
df_pedidos.to_csv(f"{PASTA_DADOS_BRUTO}/pedidos.csv", index=False, encoding="utf-8-sig")

# ================== ITENS PEDIDO ==================
itens = []
for i in range(20000):
    item = {
        "id": i+1,
        "pedido_id": random.randint(1, 8000),
        "produto_id": random.randint(1, 500),
        "quantidade": random.randint(1, 10),
        "valor_unitario": round(random.uniform(50, 5000), 2)
    }
    itens.append(item)

df_itens = pd.DataFrame(itens)
df_itens.to_csv(f"{PASTA_DADOS_BRUTO}/itens_pedido.csv", index=False, encoding="utf-8-sig")

print("✅ DADOS SUJOS GERADOS COM SUCESSO NA PASTA dados/bruto")


