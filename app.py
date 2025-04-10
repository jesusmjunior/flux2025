import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image

st.set_page_config(page_title="COGEX – Modelagem de Processos", layout="wide")

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

# === Cabeçalho institucional com logotipo maior ===
with st.container():
    col_logo, col_titulo = st.columns([1, 5])
    with col_logo:
        if os.path.exists("cogex.png"):
            st.image(Image.open("cogex.png"), width=220)
    with col_titulo:
        st.markdown("### **COGEX - CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO**")
        st.markdown("##### Sistema de Modelagem de Processos")

st.divider()

# === Seleção de JSON disponível ===
arquivos_fluxo = [f for f in os.listdir() if f.startswith("fluxo") and f.endswith(".json")]
fluxo_selecionado = st.selectbox("🔽 Selecione um fluxograma", arquivos_fluxo)

# === Carregamento do JSON ===
try:
    with open(fluxo_selecionado, encoding='utf-8') as f:
        dados = json.load(f)

    st.markdown(f"### 📌 {dados.get('titulo', 'Título não encontrado')}")

    setor_atual = dados.get("setor", setores_cogex[0])
    setor_escolhido = st.selectbox("🏛️ Setor:", setores_cogex, index=setores_cogex.index(setor_atual))

    # === Container centralizado em layout tipo A4 widescreen ===
    with st.container():
        col_fluxo, col_dados = st.columns([5, 2], gap="large")

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
