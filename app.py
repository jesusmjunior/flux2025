import streamlit as st
import json
import os

# Configuração da página
st.set_page_config(page_title="AppPy - Fluxograma COGEX", layout="wide")

# === Cabeçalho Institucional ===
col_logo, col_titulo = st.columns([1, 9])
with col_logo:
    st.image("assets/cogex.png", width=40)
with col_titulo:
    st.markdown("### **Corregedoria do Foro Extrajudicial**")
    st.markdown("##### Sistema de Visualização de Fluxogramas Jurídicos")

st.markdown("---")

# === Dropdown de Seleção de Fluxograma ===
fluxos_dir = "fluxos"
fluxo_opcoes = [f for f in os.listdir(fluxos_dir) if f.endswith(".json")]

fluxo_escolhido = st.selectbox("🔽 Selecione o Fluxograma", options=fluxo_opcoes, index=0)

# === Carregamento de Dados do Fluxograma ===
def carregar_fluxo(nome_arquivo):
    caminho = os.path.join(fluxos_dir, nome_arquivo)
    with open(caminho, encoding='utf-8') as f:
        return json.load(f)

dados_fluxo = carregar_fluxo(fluxo_escolhido)

# === Layout Triplo: Legenda | Fluxo | Base Legal ===
col_legenda, col_fluxo, col_base = st.columns([2, 6, 2])

# === Coluna: Legenda ===
with col_legenda:
    st.subheader("📘 Legenda")
    legenda = dados_fluxo.get("legenda", [])
    for item in legenda:
        st.markdown(f"- {item}")

# === Coluna: Fluxo Central ===
with col_fluxo:
    st.subheader(f"📌 {dados_fluxo.get('titulo', 'Sem Título')}")
    st.markdown(f"##### {dados_fluxo.get('subtitulo', '')}")
    st.markdown("---")
    st.markdown("### 🧭 Fluxograma")
    st.markdown(dados_fluxo.get("desenho", "Fluxo não disponível."), unsafe_allow_html=True)

# === Coluna: Base Legal ===
with col_base:
    st.subheader("⚖️ Base Legal")
    st.markdown(dados_fluxo.get("base_legal", "Não informada."))
    st.markdown("---")
    st.markdown("📁 Fluxo carregado:")
    st.code(fluxo_escolhido)
