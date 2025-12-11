# Desafio Técnico - Analytics Engineer Jr

Este repositório contém a solução para o desafio de engenharia de dados e analytics, focado na ingestão, transformação e visualização da cotação do Dólar Comercial para o ano de 2025.

## Objetivo
Construir um pipeline de dados completo (ELT) estruturado em camadas (Raw, Bronze, Analytics) e um dashboard interativo para análise da variação cambial [cite: 3-8].

## Tech Stack
- **Linguagem:** Python 3.10+
- **Bibliotecas:** Pandas, Requests, Streamlit, Plotly.
- **Visualização:** Streamlit (Execução Local) e Power BI (Análise Exploratória Extra).
- **Arquitetura:** Arquitetura de camadas (Medallion Architecture).

## Estrutura do Projeto
A organização segue o padrão sugerido de data lake local:

```text
.
├── data/
│   ├── raw/         # Arquivos JSON brutos baixados da API (12 arquivos) [cite: 26]
|   ├── bronze/      # Dado consolidado, limpo e tipado (CSV) [cite: 38]
│   └── analytics/   # Tabelas com métricas calculadas para consumo (CSV) [cite: 16]
├── src/
│   ├── ingestion.py      # Script de ingestão da API do BC
│   ├── transformation.py # Limpeza e padronização (Raw -> Bronze)
│   └── analytics.py      # Cálculo de KPIs (Bronze -> Analytics)
├── dashboard/
│   └── app.py       # Código do Dashboard Streamlit
├── main.py          # Orquestrador principal da execução [cite: 84]
├── requirements.txt # Dependências do projeto
└── README.md
