import streamlit as st
import json
import os
from PIL import Image

# === Configuração da página ===
st.set_page_config(page_title="AppPy - Fluxograma COGEX", layout="wide")

# === Logo COGEX ===
if os.path.exists("cogex.png"):
    st.image(Image.open("cogex.png"), width=40)
else:
    st.warning("⚠️ Arquivo cogex.png não encontrado.")

# === Título principal ===
st.markdown("### **Corregedoria do Foro Extrajudicial**")
st.markdown("##### Sistema de Visualização de Fluxogramas Jurídicos")
st.markdown("---")

# === Coleta arquivos de fluxo (.json) no diretório raiz ===
fluxo_opcoes = [f for f in os.listdir() if f.endswith(".json")]

fluxo_escolhido = st.selectbox("🔽 Selecione o Fluxograma", options=fluxo_opcoes, index=0)

# === Carrega os dados JSON selecionados ===
def carregar_fluxo(nome_arquivo):
    with open(nome_arquivo, encoding='utf-8') as f:
        return json.load(f)

dados_fluxo = carregar_fluxo(fluxo_escolhido)

# === Layout do conteúdo ===
col_legenda, col_fluxo, col_base = st.columns([2, 6, 2])

# === Legenda ===
with col_legenda:
    st.subheader("📘 Legenda")
    for item in dados_fluxo.get("legenda", []):
        st.markdown(f"- {item}")

# === Fluxograma ===
with col_fluxo:
    st.subheader(f"📌 {dados_fluxo.get('titulo', 'Sem Título')}")
    st.markdown(f"##### {dados_fluxo.get('subtitulo', '')}")
    st.markdown("---")
    st.markdown("### 🧭 Fluxograma")
    st.markdown(dados_fluxo.get("desenho", "Fluxo não disponível."), unsafe_allow_html=True)

# === Base Legal ===
with col_base:
    st.subheader("⚖️ Base Legal")
    st.markdown(dados_fluxo.get("base_legal", "Não informada."))
    st.markdown("---")
    st.markdown("📁 Arquivo carregado:")
    st.code(fluxo_escolhido)
