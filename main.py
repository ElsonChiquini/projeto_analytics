import os
import sys
# Importe os scripts dos arquivos (certifique-se de que os arquivos existem na pasta src)
from src.ingestion import ingest_data
from src.transformation import process_bronze_layer
from src.analytics import process_analytics_layer

def main():
    """
    Orquestrador principal do desafio Analytics Engineer.
    1. Executa a Ingestão (Raw)
    2. Executa a Transformação (Bronze)
    3. Executa a Análise (Analytics)
    4. Inicia o Dashboard (Streamlit)
    """
    print("===========================")
    print(" DESAFIO - INICIANDO       ")
    print("=========================\n")

    # 1. Etapa de Ingestão
    print(">>> [1/4] Executando Ingestão de Dados (Raw)...")
    try:
        ingest_data()
    except Exception as e:
        print(f"Erro na ingestão: {e}")
        sys.exit(1)

    # 2. Etapa de Transformação
    print("\n>>> [2/4] Executando Transformação (Bronze)...")
    try:
        process_bronze_layer()
    except Exception as e:
        print(f"Erro na transformação: {e}")
        sys.exit(1)

    # 3. Etapa de Analytics
    print("\n>>> [3/4] Gerando Métricas (Analytics)...")
    try:
        process_analytics_layer()
    except Exception as e:
        print(f"Erro na geração de métricas: {e}")
        sys.exit(1)

    # 4. Execução do Dashboard
    print("\n>>> [4/4] Inicializando Dashboard...")
    print("Pressione Ctrl+C no terminal para encerrar o servidor do Streamlit.")
    
    # Executa o comando do Streamlit usando o módulo Python para contornar o problema do PATH
    # Este comando agora garante a "Execução Local" via main.py 
    os.system("python -m streamlit run dashboard/app.py")

if __name__ == "__main__":
    main()