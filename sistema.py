import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Análise na Aviação Civil",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

#THEME
primary = "#3f41af"
secondary = "#070336"

st.markdown(f"""
<style>
    :root {{
        --primary: {primary};
        --secondary: {secondary};
    }}
</style>
""", unsafe_allow_html=True)


# CSS customizado para UI moderna
st.markdown("""
<style>
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* Importar fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Remover padding padrão */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: var(--secondary) !important;
    }
    
    /* Estilo para métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
    }
    
    /* Cards customizados */
    .custom-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    /* Título principal */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--primary) !important;
    }
    
    /* Botões */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 500;
        font-size: 1rem;
    }
    
    /* Caixa dos select/multiselect */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: var(--secondary) !important;   /* fundo do card */
        color: #000000 !important;              /* texto */
        border-radius: 8px !important;
    }

    /* Campo de entrada quando aberto */
    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        background-color: #ffffff !important;
        color: var(--primary) !important;
    }

    /* Fundo da lista dropdown */
    section[data-testid="stSidebar"] ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Tags do multiselect */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: var(--primary) !important;
        color: white !important;
        border-radius: 6px;
    }

    /* Caixa de informações (st.info) */
    section[data-testid="stSidebar"] .stAlert {
        background-color: var(--primary) !important;
        color: black !important;
        border-left: 6px solid var(--primary) !important;
    }
            
    div[data-testid="stPlotlyChart"] {
        padding-top: 0 !important;
        margin-top: -25px !important;
    }
</style>
""", unsafe_allow_html=True)

# Função para gerar dados de exemplo (substitua pelos seus dados reais)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start='2018-01-01', end='2024-12-31', freq='ME')
    
    df = pd.DataFrame({
        'data': dates,
        'acidentes': np.random.poisson(8, len(dates)),
        'incidentes': np.random.poisson(15, len(dates)),
        'tipo_aeronave': np.random.choice(['Monomotor', 'Bimotor', 'Jato', 'Helicóptero'], len(dates)),
        'regiao': np.random.choice(['Sul', 'Sudeste', 'Centro-Oeste', 'Norte', 'Nordeste'], len(dates)),
        'fase_voo': np.random.choice(['Decolagem', 'Cruzeiro', 'Pouso', 'Táxi'], len(dates)),
        'vitimas_fatais': np.random.poisson(2, len(dates)),
        'vitimas_graves': np.random.poisson(3, len(dates))
    })
    
    return df

# Carregar dados
df = load_data()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/airplane-take-off.png", width=80)
    st.markdown("🎯 Filtros de Análise")
    
    # Filtro de período
    anos = st.multiselect(
        "Período",
        options=sorted(df['data'].dt.year.unique(), reverse=True),
        default=sorted(df['data'].dt.year.unique(), reverse=True)[:3]
    )
    
    # Filtro de região
    regioes = st.multiselect(
        "Regiões",
        options=df['regiao'].unique(),
        default=df['regiao'].unique()
    )
    
    # Filtro de tipo de aeronave
    tipos = st.multiselect(
        "Tipo de Aeronave",
        options=df['tipo_aeronave'].unique(),
        default=df['tipo_aeronave'].unique()
    )
    
    st.markdown("---")
    st.markdown("### 📊 Sobre o Projeto")
    st.info("Dashboard desenvolvido para análise de dados de acidentes na aviação civil brasileira utilizando técnicas de Ciência de Dados.")
    
    st.markdown("---")
    st.markdown("**Fonte de Dados:** CENIPA")
    st.markdown("**Última atualização:** " + datetime.now().strftime("%d/%m/%Y"))

# Filtrar dados
df_filtered = df[
    (df['data'].dt.year.isin(anos)) &
    (df['regiao'].isin(regioes)) &
    (df['tipo_aeronave'].isin(tipos))
]

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<h1 class="main-title">Análise na Aviação Civil</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Uso de Dados Automatizados Para Monitoramento e Prevenção</p>', unsafe_allow_html=True)


# KPIs principais
st.markdown("### 📈 Indicadores Principais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_acidentes = df_filtered['acidentes'].sum()
    st.metric(
        label="Total de Acidentes",
        value=f"{total_acidentes:,}",
        delta=f"{((total_acidentes / df['acidentes'].sum()) - 1) * 100:.1f}%"
    )

with col2:
    total_incidentes = df_filtered['incidentes'].sum()
    st.metric(
        label="Total de Incidentes",
        value=f"{total_incidentes:,}",
        delta=f"{((total_incidentes / df['incidentes'].sum()) - 1) * 100:.1f}%"
    )

with col3:
    vitimas_fatais = df_filtered['vitimas_fatais'].sum()
    st.metric(
        label="Vítimas Fatais",
        value=f"{vitimas_fatais:,}",
        delta=f"-{abs(((vitimas_fatais / df['vitimas_fatais'].sum()) - 1) * 100):.1f}%",
        delta_color="inverse"
    )

with col4:
    taxa_fatalidade = (vitimas_fatais / total_acidentes * 100) if total_acidentes > 0 else 0
    st.metric(
        label="Taxa de Fatalidade",
        value=f"{taxa_fatalidade:.1f}%",
        delta="-2.3%",
        delta_color="inverse"
    )

st.markdown("---")

# Tabs para diferentes análises
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🗺️ Análise Regional", "✈️ Análise por Aeronave", "🔍 Análise Detalhada"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Evolução Temporal de Acidentes")
        df_timeline = df_filtered.groupby(df_filtered['data'].dt.to_period('Y')).agg({
            'acidentes': 'sum',
            'incidentes': 'sum'
        }).reset_index()
        df_timeline['data'] = df_timeline['data'].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_timeline['data'], 
            y=df_timeline['acidentes'],
            name='Acidentes',
            mode='lines+markers',
            line=dict(color='#ef4444', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=df_timeline['data'], 
            y=df_timeline['incidentes'],
            name='Incidentes',
            mode='lines+markers',
            line=dict(color='#f59e0b', width=3),
            marker=dict(size=8)
        ))
        fig.update_layout(
            height=350,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.markdown("#### Distribuição por Fase de Voo")
        df_fase = df_filtered.groupby('fase_voo')['acidentes'].sum().reset_index()
        
        fig = px.pie(
            df_fase, 
            values='acidentes', 
            names='fase_voo',
            color_discrete_sequence=px.colors.sequential.Purples_r,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            height=350,
            showlegend=True,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, width="stretch")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 5 Regiões com Mais Acidentes")
        df_regiao = df_filtered.groupby('regiao')['acidentes'].sum().sort_values(ascending=False).head(5).reset_index()
        
        fig = px.bar(
            df_regiao,
            x='acidentes',
            y='regiao',
            orientation='h',
            color='acidentes',
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            height=350,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.markdown("#### Acidentes por Tipo de Aeronave")
        df_aeronave = df_filtered.groupby('tipo_aeronave')['acidentes'].sum().reset_index()
        
        fig = px.bar(
            df_aeronave,
            x='tipo_aeronave',
            y='acidentes',
            color='tipo_aeronave',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            height=350,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, width="stretch")

with tab2:
    st.markdown("#### Análise Geográfica dos Acidentes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        df_mapa = df_filtered.groupby('regiao').agg({
            'acidentes': 'sum',
            'vitimas_fatais': 'sum',
            'vitimas_graves': 'sum'
        }).reset_index()
        
        fig = px.bar(
            df_mapa,
            x='regiao',
            y=['acidentes', 'vitimas_fatais', 'vitimas_graves'],
            barmode='group',
            color_discrete_sequence=['#667eea', '#ef4444', '#f59e0b'],
            labels={'value': 'Quantidade', 'variable': 'Categoria'}
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.markdown("##### Estatísticas Regionais")
        for regiao in df_mapa['regiao']:
            dados_regiao = df_mapa[df_mapa['regiao'] == regiao].iloc[0]
            with st.expander(f"📍 {regiao}"):
                st.metric("Acidentes", int(dados_regiao['acidentes']))
                st.metric("Vítimas Fatais", int(dados_regiao['vitimas_fatais']))
                st.metric("Vítimas Graves", int(dados_regiao['vitimas_graves']))

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Comparativo de Segurança por Aeronave")
        df_comp = df_filtered.groupby('tipo_aeronave').agg({
            'acidentes': 'sum',
            'vitimas_fatais': 'sum'
        }).reset_index()
        df_comp['taxa_fatalidade'] = (df_comp['vitimas_fatais'] / df_comp['acidentes'] * 100).round(2)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Acidentes',
            x=df_comp['tipo_aeronave'],
            y=df_comp['acidentes'],
            marker_color='#667eea'
        ))
        fig.add_trace(go.Scatter(
            name='Taxa de Fatalidade (%)',
            x=df_comp['tipo_aeronave'],
            y=df_comp['taxa_fatalidade'],
            yaxis='y2',
            mode='lines+markers',
            marker=dict(size=10, color='#ef4444'),
            line=dict(width=3, color='#ef4444')
        ))
        fig.update_layout(
            height=400,
            yaxis=dict(title='Acidentes'),
            yaxis2=dict(title='Taxa de Fatalidade (%)', overlaying='y', side='right'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified'
        )
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        st.markdown("#### Ranking de Segurança")
        df_ranking = df_comp.sort_values('taxa_fatalidade')
        
        for idx, row in df_ranking.iterrows():
            col_a, col_b, col_c = st.columns([2, 1, 1])
            with col_a:
                st.markdown(f"**{row['tipo_aeronave']}**")
            with col_b:
                st.markdown(f"🔴 {int(row['acidentes'])} acidentes")
            with col_c:
                st.markdown(f"📊 {row['taxa_fatalidade']:.1f}%")
            st.progress(min(row['taxa_fatalidade'] / 100, 1.0))

with tab4:
    st.markdown("#### Dados Detalhados")
    
    # Filtros adicionais
    col1, col2, col3 = st.columns(3)
    with col1:
        fase_filtro = st.selectbox("Filtrar por Fase de Voo", ["Todas"] + list(df_filtered['fase_voo'].unique()))
    with col2:
        tipo_filtro = st.selectbox("Filtrar por Tipo", ["Todos"] + list(df_filtered['tipo_aeronave'].unique()))
    with col3:
        regiao_filtro = st.selectbox("Filtrar por Região", ["Todas"] + list(df_filtered['regiao'].unique()))
    
    # Aplicar filtros adicionais
    df_tabela = df_filtered.copy()
    if fase_filtro != "Todas":
        df_tabela = df_tabela[df_tabela['fase_voo'] == fase_filtro]
    if tipo_filtro != "Todos":
        df_tabela = df_tabela[df_tabela['tipo_aeronave'] == tipo_filtro]
    if regiao_filtro != "Todas":
        df_tabela = df_tabela[df_tabela['regiao'] == regiao_filtro]
    
    # Exibir tabela
    st.dataframe(
        df_tabela.sort_values('data', ascending=False),
        width="stretch",
        height=400
    )
    
    # Botão de download
    csv = df_tabela.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download dos Dados (CSV)",
        data=csv,
        file_name=f"acidentes_aviacao_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #3f41af; padding: 2rem 0; height: 100px'>
    <p>Desenvolvido para TCC - Análise da Segurança Operacional na Aviação Civil</p>
    <p>Ciência de Dados | Python | Streamlit</p>
</div>
""", unsafe_allow_html=True)