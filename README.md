### 📊 Aura Hardware — Data Analytics & Dashboard Project

O Aura Hardware é um projeto completo de engenharia e análise de dados, que simula o ambiente real de uma empresa de hardware, desde a geração de dados sujos, passando por modelagem, limpeza, métricas de negócio, até a visualização interativa utilizando Streamlit.

O objetivo principal do projeto é demonstrar como dados bem tratados podem apoiar a tomada de decisões estratégicas, oferecendo insights claros sobre faturamento, vendas, clientes e estoque.

---
### 🧱 Arquitetura do Projeto
```
Aura-Hardware/
│
├── config/
│   └── config.py
│
├── dados/
│   ├── bruto/      → Dados sujos (raw data)
│   └── limpo/      → Dados tratados e prontos para análise
│
├── scripts/
│   ├── 01_gerar_dados.py
│   ├── 02_criar_banco.py
│   ├── 03_limpeza_dados.py
│   └── 04_metricas.py
│
├── dashboard.py
└── README.md
```
Essa separação facilita:
- manutenção do projeto
- reaproveitamento de código
- escalabilidade
- entendimento rápido do fluxo de dados

---
### 🔄 Pipeline de Dados (End-to-End)

**Geração de Dados (Dados Brutos)**

O script 01_gerar_dados.py utiliza a biblioteca Faker para gerar dados realistas, porém intencionalmente sujos, simulando problemas comuns do mundo real, como:

- emails inválidos ou ausentes
- nomes com espaços extras
- CPFs duplicados
- estoque negativo
- dados nulos
- formatos inconsistentes

Esses dados são salvos em `dados/bruto/`.

📌 Simula fielmente a realidade de sistemas legados e múltiplas fontes de dados.

---
**Limpeza e Padronização dos Dados**

O script 03_limpeza_dados.py realiza o tratamento dos dados, incluindo:

- remoção de duplicidades (CPF)
- validação de emails
- padronização de CEP
- conversão correta de datas
- correção de tipos numéricos
- regras de negócio (ex: apenas clientes maiores de idade)

Os dados limpos são exportados para `dados/limpo/`.

📌 Garante dados confiáveis para análises e evita decisões baseadas em informações incorretas.

---
**Geração de Métricas de Negócio**

O script 04_metricas.py cria indicadores estratégicos, como:

- 📈 Faturamento mensal

- 💳 Ticket médio por cliente

- 🔥 Produtos mais vendidos

- 🏆 Clientes com maior volume de compras

- ⚠️ Alerta de estoque baixo

- 👥 Base de clientes segmentada

📌 Transforma dados operacionais em informação estratégica.

---
📊 Dashboard Interativo (Streamlit)

O arquivo dashboard.py apresenta os dados de forma visual, em um dashboard dark corporativo, inspirado em Power BI.

- 🔹 KPIs Principais
- 💰 Faturamento Total
- 📦 Total de Produtos Vendidos
- 👥 Total de Clientes

Esses indicadores permitem uma visão rápida do desempenho do negócio.





