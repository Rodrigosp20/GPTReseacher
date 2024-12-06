import asyncio
import os
from gpt_researcher import GPTResearcher
from detailed_report import DetailedReport

import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
os.environ["FAST_LLM"] = st.secrets["FAST_LLM"]
os.environ["SMART_LLM"] = st.secrets["SMART_LLM"]

st.set_page_config(
    page_title="GPT Researcher",
    page_icon="🕵",
)


def is_loading():
    return st.session_state.loading if 'loading' in st.session_state else False


async def detailed_research(user_input):

    detailed_report = DetailedReport(
        query=user_input,
        report_type="research_report",
    )

    report = await detailed_report.run()

    st.session_state.research = report
    st.session_state.loading = False
    st.rerun()


async def research(user_input):

    researcher = GPTResearcher(
        query=user_input,
        report_type="detailed_report",
    )

    await researcher.conduct_research()
    report = await researcher.write_report()

    st.session_state.research = report
    st.session_state.loading = False
    st.rerun()

st.markdown("""
    <style>
        .stHorizontalBlock {
            align-items: center !important
        }
        
        .stHorizontalBlock h1 {
            margin-top: -8px;
        }
    </style>
""", unsafe_allow_html=True)

c1, c2 = st.columns([0.4, 0.6])
c1.image("https://streamconsulting.pt/img/logo_dark.png",
         use_container_width=True)
c2.title("GPT Researcher")

loading = is_loading()

is_detailed = st.toggle("Report Detalhado", value=True)

empresa = st.text_input(
    "Nome Empresa", value=st.query_params.get('nome'), disabled=loading)
nif = st.text_input(
    "NIF Empresa", value=st.query_params.get('nif'), disabled=loading)
website = st.text_input(
    "Website", value=st.query_params.get('website'), disabled=loading)
dimensao = st.text_input(
    "Dimensao da Empresa", value=st.query_params.get('dimensao'), disabled=loading)
objetivos = st.text_area(
    "Objetivos Projeto", value=st.query_params.get('objetivos'), disabled=loading)
mercados = st.text_input(
    "Marcados-Alvo", value=st.query_params.get('mercados'), disabled=loading)
cae = st.text_input(
    "CAE do Projeto", value=st.query_params.get('cae'), disabled=loading)
produto = st.text_input("Produto", disabled=loading)

if st.button("Research", use_container_width=True, disabled=loading):

    st.session_state.loading = True
    st.rerun()

if loading:
    prompt = f"""
Empresa: {empresa}
NIF: {nif}
Website: {website if website.strip() else 'N/A'}
Dimensão da Empresa: {dimensao}
Objetivos do Projeto: {objetivos}
Mercados-Alvo: {mercados}
Produto: {produto}
CAE: {cae}

- Resumo/Análise do contexto empresarial da empresa (recorrendo ao website da empresa, caso aplicável) bem como da atividade desenvolvida e evolução nos 5 anos anteriores
- Pesquisa e recolher dados atualizados e relevantes sobre o setor/CAE do projeto, com foco nas seguintes áreas:
    >Tendências de mercado: Identificar tendências e mudanças significativas no setor ou CAE do projeto.
    >Evolução dos mercados-alvo: Coletar e comparar dados sobre a evolução das exportações para os países-alvo identificados no projeto, em comparação com o mercado português.
    >Exportação do produto-alvo: Obter dados de exportação para o produto específico do projeto. Analisar a evolução desse produto nos mercados-alvo e em Portugal.
    >Quadros do Setor: Analisar os quadros do setor para avaliar o índice de exportações (IE) das empresas nacionais do setor. Extraiar variações percentuais e outros indicadores financeiros relevantes para apoiar a tomada de decisão.

Rescreve o relatório em PT-PT, apresentando todas as informações recolhidas de forma organizada, destacando variações, tendências e informações que possam ser úteis para a elaboração de relatórios financeiros e estudos de mercado."""

    if is_detailed:
        asyncio.run(detailed_research(prompt))
    else:
        asyncio.run(research(prompt))


if "research" in st.session_state:
    copy_html = f"""
    <button onclick="navigator.clipboard.writeText(`{st.session_state.research}`).then(() => alert('Text copied to clipboard!'))" >
        Copy to Clipboard
    </button>
"""

    # Embed the HTML
    st.components.v1.html(copy_html, height=50)

    st.markdown(st.session_state.research)
