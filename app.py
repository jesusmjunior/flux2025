import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image

st.set_page_config(page_title="COGEX – Modelagem de Processos", layout="wide")

# === Cabeçalho institucional ===
col_logo, col_texto = st.columns([1, 9])
with col_logo:
    if os.path.exists("cogex.png"):
        st.image(Image.open("cogex.png"), width=120)
with col_texto:
    st.markdown("### **Corregedoria do Foro Extrajudicial**")
    st.markdown("##### Sistema de Modelagem de Processos - COGEX")

st.markdown("---")

# === Dropdown de seleção de fluxo ===
arquivos_fluxo = [f for f in os.listdir() if f.startswith("fluxo") and f.endswith(".json")]
fluxo_selecionado = st.selectbox("🔽 Selecione um fluxograma", arquivos_fluxo)

# === Carregar JSON ===
with open(fluxo_selecionado, encoding='utf-8') as f:
    dados = json.load(f)

st.subheader(f"📌 {dados.get('titulo', 'Sem título')}")
st.markdown(f"#### {dados.get('subtitulo', '')}")

# === Grid visual 8:4 ===
col1, col2 = st.columns([8, 4])

# === Renderizador gráfico BPMN ===
with col1:
    fluxo = Digraph('Fluxograma', format='png')
    fluxo.attr(rankdir='TB', size='6,8', nodesep='0.5', dpi='150')  # tamanho equilibrado

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

    # === Exportação protegida ===
    try:
        nome_img = fluxo_selecionado.replace(".json", "_exportado")
        caminho_final = fluxo.render(nome_img, cleanup=False)
        with open(caminho_final, "rb") as img_file:
            st.download_button("📥 Baixar Fluxograma PNG", img_file,
                               file_name=os.path.basename(caminho_final),
                               mime="image/png")
    except Exception as e:
        st.error("❌ Erro ao exportar PNG: " + str(e))

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
