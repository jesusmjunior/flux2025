import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image

st.set_page_config(page_title="COGEX – Modelagem de Processos", layout="wide")

# === Cabeçalho institucional com logo ===
col_logo, col_texto = st.columns([1, 9])
with col_logo:
    if os.path.exists("cogex.png"):
        st.image(Image.open("cogex.png"), width=120)  # Logo em tamanho maior
with col_texto:
    st.markdown("### **Corregedoria do Foro Extrajudicial**")
    st.markdown("##### Sistema de Modelagem de Processos - COGEX")

st.markdown("---")

# === Dropdown para seleção de fluxos ===
arquivos_fluxo = [f for f in os.listdir() if f.startswith("fluxo") and f.endswith(".json")]
fluxo_selecionado = st.selectbox("🔽 Selecione um fluxograma", arquivos_fluxo)

# === Carregamento do JSON selecionado ===
with open(fluxo_selecionado, encoding='utf-8') as f:
    dados = json.load(f)

st.subheader(f"📌 {dados.get('titulo', 'Sem título')}")
st.markdown(f"#### {dados.get('subtitulo', '')}")

col1, col2 = st.columns([3, 1])

# === Geração do fluxograma BPMN ===
with col1:
    fluxo = Digraph('Fluxograma', format='png')
    fluxo.attr(rankdir='TB', size='7,9', nodesep='0.6', dpi='150')

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

    # === Exportação do PNG ===
    nome_img = fluxo_selecionado.replace(".json", "_exportado")
    caminho_final = fluxo.render(nome_img, cleanup=False)
    with open(caminho_final, "rb") as img_file:
        st.download_button("📥 Baixar Fluxograma PNG", img_file,
                           file_name=os.path.basename(caminho_final),
                           mime="image/png")

# === Legenda + Base Legal ===
with col2:
    st.subheader("📘 Legenda")
    for tipo, estilo in estilo_map.items():
        simbolo = "⬤" if estilo["shape"] == "circle" else "⬛"
        cor = estilo["fillcolor"]
        st.markdown(f"{simbolo} **{tipo.capitalize()}** – cor `{cor}`")

    st.markdown("---")
    st.subheader("⚖️ Base Legal")
    st.markdown(dados.get("base_legal", "Não informada."))
