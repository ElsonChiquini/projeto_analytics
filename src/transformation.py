import pandas as pd
import os
import glob
import json

# Configurações de Caminhos
INPUT_PATH = "data/raw/dolar/*.json"
OUTPUT_DIR = "data/bronze/dolar"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "dolar_2025.csv")

def process_bronze_layer():
    """
    Lê os arquivos JSON da camada Raw, consolida em um único DataFrame,
    realiza a limpeza e padronização dos dados e salva na camada Bronze.
    """
    print("--- Iniciando processamento da Camada Bronze ---")

    # 1. Listar todos os arquivos JSON da pasta raw
    json_files = glob.glob(INPUT_PATH)
    
    if not json_files:
        print("✗ Nenhum arquivo encontrado em data/raw/dolar/")
        return

    data_frames = []

    # 2. Ler cada arquivo e adicionar à lista
    for file in json_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Converte o JSON direto para DataFrame
                df_temp = pd.DataFrame(data)
                data_frames.append(df_temp)
        except Exception as e:
            print(f"Erro ao ler arquivo {file}: {e}")

    if not data_frames:
        print("✗ Não foi possível carregar os dataframes.")
        return

    # 3. Consolidar em uma tabela única 
    df_consolidado = pd.concat(data_frames, ignore_index=True)
    
    print(f"Registros brutos carregados: {len(df_consolidado)}")

    # 4. Limpeza e Padronização 
    
    # Padronizar Data: Converter string "DD/MM/AAAA" para objeto datetime
    # Isso permite ordenar cronologicamente de verdade
    df_consolidado['data'] = pd.to_datetime(df_consolidado['data'], format='%d/%m/%Y')

    # Padronizar Valor: 
    if df_consolidado['valor'].dtype == 'object':
        df_consolidado['valor'] = df_consolidado['valor'].astype(str).str.replace(',', '.')
        df_consolidado['valor'] = pd.to_numeric(df_consolidado['valor'])

    # Remover duplicatas 
    df_consolidado = df_consolidado.drop_duplicates()

    # Ordenar por data
    df_consolidado = df_consolidado.sort_values(by='data').reset_index(drop=True)

    # 5. Salvar na camada Bronze
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_consolidado.to_csv(OUTPUT_FILE, index=False)
    
    print(f"✓ Sucesso: Arquivo salvo em {OUTPUT_FILE}")
    print(f"Total de registros finais: {len(df_consolidado)}")
    print(df_consolidado.head()) # Mostra as primeiras linhas para conferência

if __name__ == "__main__":
    process_bronze_layer()