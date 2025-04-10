import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image

st.set_page_config(page_title="Fluxo BPMN COGEX", layout="wide")

# Cabeçalho
st.markdown("### Corregedoria do Foro Extrajudicial")
st.markdown("##### Sistema de Modelagem de Processos - COGEX")

if os.path.exists("cogex.png"):
    st.image(Image.open("cogex.png"), width=40)

st.markdown("---")

# Carregar JSON
with open("fluxo2.json", encoding='utf-8') as f:
    dados = json.load(f)

st.subheader(f"📌 {dados['titulo']}")
st.markdown(f"#### {dados['subtitulo']}")

col1, col2 = st.columns([3, 1])

# Renderizador BPMN por código
with col1:
    fluxo = Digraph('Fluxograma', format='png')
    fluxo.attr(rankdir='TB', size='8,10', nodesep='0.5')

    estilo_map = {
        "inicio":     {"shape": "circle", "style": "filled", "fillcolor": "lightgreen"},
        "tarefa":     {"shape": "box", "style": "rounded,filled", "fillcolor": "lightblue"},
        "verificacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "khaki"},
        "publicacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "lightpink"},
        "fiscalizacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "lightgrey"},
        "fim":        {"shape": "doublecircle", "style": "filled", "fillcolor": "red"}
    }

    for etapa in dados["etapas"]:
        estilo = estilo_map.get(etapa["tipo"], {})
        fluxo.node(etapa["id"], etapa["texto"], **estilo)

    for origem, destino in dados["conexoes"]:
        fluxo.edge(origem, destino)

    st.graphviz_chart(fluxo)

# Legenda + Base Legal
with col2:
    st.subheader("📘 Legenda")
    for tipo, estilo in estilo_map.items():
        cor = estilo['fillcolor']
        simbolo = "⬤" if "circle" in estilo["shape"] else "⬛"
        st.markdown(f"{simbolo} **{tipo.capitalize()}** – cor `{cor}`")

    st.markdown("---")
    st.subheader("⚖️ Base Legal")
    st.markdown(dados["base_legal"])
