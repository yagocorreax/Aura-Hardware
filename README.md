📊 Aura Hardware — Data Analytics & Dashboard Project

O Aura Hardware é um projeto completo de engenharia e análise de dados, que simula o ambiente real de uma empresa de hardware, desde a geração de dados sujos, passando por modelagem, limpeza, métricas de negócio, até a visualização interativa utilizando Streamlit.

O objetivo principal do projeto é demonstrar como dados bem tratados podem apoiar a tomada de decisões estratégicas, oferecendo insights claros sobre faturamento, vendas, clientes e estoque.

---
🧱 Arquitetura do Projeto
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

