import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image

st.set_page_config(page_title="COGEX – Modelagem de Processos", layout="centered")

# === Lista oficial de setores da COGEX ===
setores_cogex = [
    "Gabinete dos Juízes Corregedores",
    "Núcleo de Registro Civil",
    "Núcleo de Atos",
    "Diretoria do COGEX",
    "Chefe de Gabinete dos Juízes Corregedores",
    "Assessoria Jurídica",
    "Coordenadoria de Serventias Extrajudiciais",
    "Coordenadoria de Reclamações e Processos Disciplinares",
    "Coordenadoria Administrativa",
    "Coordenadoria de Inspeções",
    "Coordenadoria de Análise de Contas"
]

# === CSS A4 Vertical Centered ===
st.markdown("""
    <style>
    .main {
        max-width: 850px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Cabeçalho com logotipo institucional ===
col_logo, col_texto = st.columns([1, 4])
with col_logo:
    if os.path.exists("cogex.png"):
        st.image(Image.open("cogex.png"), width=200)
with col_texto:
    st.markdown("### **COGEX - CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO**")
    st.markdown("##### Sistema de Modelagem de Processos")

st.divider()

# === Seleção do fluxo ===
arquivos_fluxo = [f for f in os.listdir() if f.startswith("fluxo") and f.endswith(".json")]
fluxo_selecionado = st.selectbox("🔽 Selecione um fluxograma", arquivos_fluxo)

# === Carregamento do fluxo selecionado ===
try:
    with open(fluxo_selecionado, encoding='utf-8') as f:
        dados = json.load(f)

    st.subheader(f"📌 {dados.get('titulo', 'Título não encontrado')}")
    
    setor_atual = dados.get("setor", setores_cogex[0])
    st.selectbox("🏛️ Setor:", setores_cogex, index=setores_cogex.index(setor_atual), disabled=True)

    # === Renderização centralizada ===
    col_fluxo, col_dados = st.columns([2.5, 1], gap="medium")

    with col_fluxo:
        fluxo = Digraph('Fluxograma', format='png')
        fluxo.attr(rankdir='TB', size='8,10', nodesep='0.5')

        estilo_map = {
            "inicio": {"shape": "circle", "style": "filled", "fillcolor": "lightgreen"},
            "tarefa": {"shape": "box", "style": "rounded,filled", "fillcolor": "lightblue"},
            "verificacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "khaki"},
            "publicacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "lightpink"},
            "fiscalizacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "lightgrey"},
            "fim": {"shape": "doublecircle", "style": "filled", "fillcolor": "red"}
        }

        for etapa in dados["etapas"]:
            estilo = estilo_map.get(etapa["tipo"], {})
            fluxo.node(etapa["id"], etapa["texto"], **estilo)

        for origem, destino in dados["conexoes"]:
            fluxo.edge(origem, destino)

        st.graphviz_chart(fluxo)

    with col_dados:
        st.subheader("📘 Legenda")
        for tipo, estilo in estilo_map.items():
            cor = estilo['fillcolor']
            simbolo = "⬤" if estilo["shape"] == "circle" else "⬛"
            st.markdown(f"{simbolo} **{tipo.capitalize()}** – cor `{cor}`")

        st.markdown("---")
        st.subheader("⚖️ Base Legal")
        st.markdown(dados.get("base_legal", "Não informada."))

except Exception as e:
    st.error(f"❌ Erro ao carregar ou renderizar o fluxo: {str(e)}")
