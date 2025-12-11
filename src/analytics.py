import pandas as pd
import os

# Configurações de Caminhos
INPUT_FILE = "data/bronze/dolar/dolar_2025.csv"
OUTPUT_DIR = "data/analytics/dolar"
DAILY_OUTPUT = os.path.join(OUTPUT_DIR, "dolar_daily.csv")
MONTHLY_OUTPUT = os.path.join(OUTPUT_DIR, "dolar_monthly.csv")

def process_analytics_layer():
    """
    Gera as métricas analíticas a partir da camada Bronze.
    Cria tabelas para visão diária (com médias móveis) e visão mensal (agregações).
    """
    print("--- Iniciando processamento da Camada Analytics ---")

    # 1. Carregar dados da camada Bronze
    if not os.path.exists(INPUT_FILE):
        print(f"✗ Arquivo não encontrado: {INPUT_FILE}. Rode a camada bronze antes.")
        return

    df = pd.read_csv(INPUT_FILE)
    df['data'] = pd.to_datetime(df['data']) # Garante que é data
    
    # ---------------------------------------------------------
    # PARTE 1: Métricas Diárias
    # ---------------------------------------------------------
    
    # Ordenar por segurança
    df = df.sort_values(by='data')

    # Métrica 1: Variação Percentual Diária (%)
    # Mostra o quanto o dólar subiu ou caiu em relação ao dia anterior
    df['variacao_pct'] = df['valor'].pct_change() * 100

    # Métrica 2: Média Móvel de 7 dias
    # Suaviza as oscilações diárias para mostrar a tendência da semana
    df['media_movel_7d'] = df['valor'].rolling(window=7).mean()

    # Salvar tabela diária
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df.to_csv(DAILY_OUTPUT, index=False)
    print(f"✓ Tabela diária salva: {DAILY_OUTPUT}")

    # ---------------------------------------------------------
    # PARTE 2: Métricas Mensais (Agregadas)
    # ---------------------------------------------------------
    
    # Extrair o mês para agrupar
    df['mes'] = df['data'].dt.to_period('M')

    # Agregação: Média, Mínima, Máxima e Desvio Padrão (Volatilidade)
    df_monthly = df.groupby('mes')['valor'].agg(
        media_mensal='mean',
        minima_mensal='min',
        maxima_mensal='max',
        volatilidade='std'  # Desvio padrão como proxy de volatilidade
    ).reset_index()

    # Transformar a coluna 'mes' de volta para string ou timestamp para salvar
    df_monthly['mes'] = df_monthly['mes'].astype(str)

    # Salvar tabela mensal
    df_monthly.to_csv(MONTHLY_OUTPUT, index=False)
    print(f"✓ Tabela mensal salva: {MONTHLY_OUTPUT}")
    
    # Preview
    print("\n--- Preview Mensal ---")
    print(df_monthly.head())

if __name__ == "__main__":
    process_analytics_layer()