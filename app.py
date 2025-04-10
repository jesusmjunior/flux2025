import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image
import base64

st.set_page_config(page_title="COGEX – Modelagem de Processos", layout="wide")

# === Cabeçalho Institucional ===
col_logo, col_texto = st.columns([1, 9])
with col_logo:
    if os.path.exists("cogex.png"):
        st.image(Image.open("cogex.png"), width=120)
with col_texto:
    st.markdown("### **COGEX - CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO**")
    st.markdown("##### Sistema de Modelagem de Processos")

st.markdown("---")

# === Dropdown para múltiplos fluxos ===
arquivos_fluxo = [f for f in os.listdir() if f.startswith("fluxo") and f.endswith(".json")]
fluxo_selecionado = st.selectbox("🔽 Selecione um fluxograma", arquivos_fluxo)

# === Carregar o fluxo selecionado ===
try:
    with open(fluxo_selecionado, encoding='utf-8') as f:
        dados = json.load(f)

    st.subheader(f"📌 {dados.get('titulo', 'Título não encontrado')}")
    st.markdown(f"**🏛️ Setor:** {dados.get('setor', 'Setor não informado')}")

    col1, col2 = st.columns([3, 1])

    # === Fluxograma ===
    with col1:
        fluxo = Digraph('Fluxograma', format='png')
        fluxo.attr(rankdir='TB', size='8,10', nodesep='0.5', dpi='150')

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

        # Exportar imagem
        nome_img = fluxo_selecionado.replace(".json", "_fluxo")
        caminho_img = fluxo.render(nome_img, cleanup=False)

        # === Botão para exportar HTML institucional ===
        with open(caminho_img, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        html_final = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>{dados.get('titulo')}</title>
        </head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 40px;">
            <h2 style="margin-bottom: 0;">COGEX - CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO</h2>
            <h3 style="margin: 4px 0;">{dados.get('titulo')}</h3>
            <p style="margin: 4px 0; font-size: 14px;"><strong>Setor:</strong> {dados.get('setor')}</p>
            <hr style="margin: 20px 0;">
            <img src="data:image/png;base64,{img_base64}" style="width:70%; max-width:800px; height:auto; margin: 20px auto;" />
            <hr style="margin-top: 40px;">
            <footer style="font-size: 12px; color: #555;">Documento gerado automaticamente por AppPy-Cogex ©</footer>
        </body>
        </html>
        """

        html_path = f"{nome_img}_exportado.html"
        with open(html_path, "w", encoding="utf-8") as f_html:
            f_html.write(html_final)

        with open(html_path, "rb") as f_html:
            st.download_button("🌐 Baixar HTML Institucional", data=f_html,
                               file_name=os.path.basename(html_path),
                               mime="text/html")

    # === Legenda + Base Legal ===
    with col2:
        st.subheader("📘 Legenda")
        for tipo, estilo in estilo_map.items():
            simbolo = "⬤" if estilo["shape"] == "circle" else "⬛"
            cor = estilo['fillcolor']
            st.markdown(f"{simbolo} **{tipo.capitalize()}** – cor `{cor}`")

        st.markdown("---")
        st.subheader("⚖️ Base Legal")
        st.markdown(dados.get("base_legal", "Não informada."))

except Exception as e:
    st.error(f"❌ Erro ao carregar ou renderizar o fluxo: {str(e)}")
