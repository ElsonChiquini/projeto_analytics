import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da Página
st.set_page_config(page_title="Dashboard Dólar 2025", layout="wide")

# Título e Descrição
st.title("Painel de Monitoramento do Dólar - 2025")
st.markdown("Este dashboard consome dados da camada Analytics para monitorar a cotação do dólar.")

# --- CARREGAMENTO DE DADOS ---
# Função com cache para não recarregar os dados a cada clique
@st.cache_data
def load_data():
    # Caminhos relativos baseados na execução do main.py na raiz
    daily_path = "data/analytics/dolar/dolar_daily.csv"
    monthly_path = "data/analytics/dolar/dolar_monthly.csv"
    
    # Verifica se arquivos existem
    if not os.path.exists(daily_path) or not os.path.exists(monthly_path):
        return None, None

    df_daily = pd.read_csv(daily_path)
    df_monthly = pd.read_csv(monthly_path)
    
    # Converter colunas de data
    df_daily['data'] = pd.to_datetime(df_daily['data'])
    
    return df_daily, df_monthly

df_daily, df_monthly = load_data()

if df_daily is None:
    st.error("Erro: Arquivos da camada Analytics não encontrados. Rode 'python main.py' primeiro.")
    st.stop()

# --- SIDEBAR (FILTROS) ---
st.sidebar.header("Filtros")

# Filtro de Mês
# Extrair lista de meses disponíveis
df_daily['mes_nome'] = df_daily['data'].dt.strftime('%B') # Nome do mês
df_daily['mes_num'] = df_daily['data'].dt.month
lista_meses = df_daily['mes_num'].unique()
lista_meses_nomes = df_daily['mes_nome'].unique()

mes_selecionado = st.sidebar.selectbox("Selecione o Mês", lista_meses, format_func=lambda x: f"Mês {x}")

# Filtrar dados com base na seleção
df_filtrado = df_daily[df_daily['mes_num'] == mes_selecionado]

# --- KPI's (INDICADORES NUMÉRICOS) ---
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

# Cálculos para os cartões
media_mes = df_filtrado['valor'].mean()
max_mes = df_filtrado['valor'].max()
min_mes = df_filtrado['valor'].min()
volatilidade = df_filtrado['valor'].std()

col1.metric("Cotação Média", f"R$ {media_mes:.2f}")
col2.metric("Máxima do Mês", f"R$ {max_mes:.2f}")
col3.metric("Mínima do Mês", f"R$ {min_mes:.2f}")
col4.metric("Volatilidade", f"{volatilidade:.3f}")

# --- GRÁFICOS ---
st.markdown("### Evolução Diária da Cotação")

# Gráfico de Linha com Plotly
fig_line = px.line(df_filtrado, x='data', y=['valor', 'media_movel_7d'], 
                   labels={'value': 'Valor (R$)', 'data': 'Data', 'variable': 'Indicador'},
                   title=f"Dólar Comercial vs Média Móvel (Mês {mes_selecionado})")
fig_line.update_layout(hovermode="x unified")
st.plotly_chart(fig_line, use_container_width=True)

# Gráfico de Variação Percentual
st.markdown("### Variação Percentual Diária (%)")
fig_bar = px.bar(df_filtrado, x='data', y='variacao_pct',
                 color='variacao_pct',
                 color_continuous_scale=px.colors.diverging.RdYlGn,
                 labels={'variacao_pct': 'Variação %'},
                 title="Volatilidade Diária (Cores indicam intensidade)")
st.plotly_chart(fig_bar, use_container_width=True)