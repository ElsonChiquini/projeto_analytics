import os
import json
import requests
import calendar
from datetime import datetime

# Configurações Iniciais
BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados"
OUTPUT_DIR = "data/raw/dolar"
YEAR = 2025

def ingest_data():
    """
    Realiza a ingestão mensal dos dados de Dólar para o ano de 2025.
    Salva os arquivos na camada raw.
    """
    print(f"--- Iniciando ingestão para o ano {YEAR} ---")
    
    # Garante que o diretório existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Loop para os 12 meses do ano 
    for month in range(1, 13):
        
        # Calcula o último dia do mês para montar a data correta
        # calendar.monthrange retorna (dia_semana, ultimo_dia)
        last_day = calendar.monthrange(YEAR, month)[1]
        
        # Formata datas no padrão da API: DD/MM/AAAA
        start_date = f"01/{month:02d}/{YEAR}"
        end_date = f"{last_day}/{month:02d}/{YEAR}"
        
        # Monta a URL com os parâmetros
        params = {
            "formato": "json",
            "dataInicial": start_date,
            "dataFinal": end_date
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status() # Alerta se der erro 404 ou 500
            
            data = response.json()
            
            # Define o nome do arquivo: MM-2025.json
            file_name = f"{month:02d}-{YEAR}.json"
            file_path = os.path.join(OUTPUT_DIR, file_name)
            
            # Salva o arquivo exatamente como retornado
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            print(f"✓ Sucesso: {file_name} salvo com {len(data)} registros.")

        except Exception as e:
            print(f"✗ Erro ao baixar dados de {month}/{YEAR}: {e}")

if __name__ == "__main__":
    ingest_data()