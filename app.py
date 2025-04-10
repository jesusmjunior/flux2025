import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image
import base64

st.set_page_config(page_title="Fluxo BPMN COGEX", layout="wide")

# === Cabeçalho ===
col_logo, col_texto = st.columns([1, 9])
with col_logo:
    if os.path.exists("cogex.png"):
        st.image(Image.open("cogex.png"), width=120)
with col_texto:
    st.markdown("### **Corregedoria do Foro Extrajudicial**")
    st.markdown("##### Sistema de Modelagem de Processos - COGEX")
st.markdown("---")

# === Detectar fluxos JSON ===
arquivos_fluxo = [f for f in os.listdir() if f.startswith("fluxo") and f.endswith(".json")]
fluxo_selecionado = st.selectbox("🔽 Selecione um fluxograma", arquivos_fluxo)

# === Carregar JSON selecionado ===
with open(fluxo_selecionado, encoding='utf-8') as f:
    dados = json.load(f)

st.subheader(f"📌 {dados['titulo']}")
st.markdown(f"#### {dados['subtitulo']}")

col1, col2 = st.columns([3, 1])

# === Renderizador BPMN ===
with col1:
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

    # === Exibição do fluxo ===
    st.graphviz_chart(fluxo)

    # === Exportação PNG ===
    nome_img = fluxo_selecionado.replace(".json", "_fluxo")
    caminho_img = fluxo.render(nome_img, cleanup=False)
    with open(caminho_img, "rb") as f_img:
        btn = st.download_button(
            label="📥 Baixar Fluxograma PNG",
            data=f_img,
            file_name=os.path.basename(caminho_img),
            mime="image/png"
        )

    # === Exportação PDF via workaround base64 ===
    try:
        import pdfkit
        html = f"<img src='data:image/png;base64,{base64.b64encode(open(caminho_img, 'rb').read()).decode()}' />"
        pdfkit.from_string(html, nome_img + ".pdf")
        with open(nome_img + ".pdf", "rb") as fpdf:
            st.download_button(
                label="📄 Baixar como PDF",
                data=fpdf,
                file_name=nome_img + ".pdf",
                mime="application/pdf"
            )
    except Exception as e:
        st.warning("PDF não gerado (pdfkit não instalado ou falhou).")

# === Legenda + Base Legal ===
with col2:
    st.subheader("📘 Legenda")
    for tipo, estilo in estilo_map.items():
        cor = estilo['fillcolor']
        simbolo = "⬤" if estilo["shape"] == "circle" else "⬛"
        st.markdown(f"{simbolo} **{tipo.capitalize()}** – cor `{cor}`")

    st.markdown("---")
    st.subheader("⚖️ Base Legal")
    st.markdown(dados["base_legal"])
