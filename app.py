import streamlit as st
import json
from PIL import Image
import os

st.set_page_config(page_title="Fluxograma COGEX BPMN", layout="wide")

# Cabeçalho
st.markdown("## Corregedoria do Foro Extrajudicial")
st.markdown("##### Sistema de Modelagem de Processos - COGEX")
if os.path.exists("cogex.png"):
    st.image("cogex.png", width=40)

st.markdown("---")

# Carregar dados do fluxo2.json
with open("fluxo2.json", encoding='utf-8') as f:
    dados = json.load(f)

# Layout triplo
col_legenda, col_fluxo, col_base = st.columns([2, 6, 2])

# Legenda
with col_legenda:
    st.subheader("📘 Legenda")
    for item in dados.get("legenda", []):
        st.markdown(f"- {item}")

# Imagem do fluxograma
with col_fluxo:
    st.subheader(f"📌 {dados.get('titulo', '')}")
    st.markdown(f"##### {dados.get('subtitulo', '')}")
    st.image("fluxograma_cogex.png", use_column_width=True)

# Base legal
with col_base:
    st.subheader("⚖️ Base Legal")
    st.markdown(dados.get("base_legal", ""))
    st.markdown("✅ Provimento nº 33/2024 – CGJ/MA")

