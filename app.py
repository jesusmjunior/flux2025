
import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image
from datetime import datetime
import base64

st.set_page_config(page_title="COGEX – Modelagem de Processos", layout="centered")

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

st.markdown("""
    <style>
    .main {
        max-width: 850px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

col_logo, col_texto = st.columns([1, 4])
with col_logo:
    if os.path.exists("cogex.png"):
        st.image(Image.open("cogex.png"), width=200)
with col_texto:
    st.markdown("### **COGEX - CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO**")
    st.markdown("##### Sistema de Modelagem de Processos")

st.divider()

arquivos_fluxo = [f for f in os.listdir() if f.startswith("fluxo") and f.endswith(".json")]
fluxo_selecionado = st.selectbox("🔽 Selecione um fluxograma", arquivos_fluxo)

try:
    with open(fluxo_selecionado, encoding='utf-8') as f:
        dados = json.load(f)

    st.subheader(f"📌 {dados.get('titulo', 'Título não encontrado')}")
    setor_atual = dados.get("setor", setores_cogex[0])
    setor_escolhido = st.selectbox("🏛️ Setor:", setores_cogex, index=setores_cogex.index(setor_atual))

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

    st.markdown("---")
    if st.button("📤 Exportar com desenho real do fluxo (HTML)"):

        for etapa in dados["etapas"]:
            estilo = estilo_map.get(etapa["tipo"], {})
            fluxo.node(etapa["id"], etapa["texto"], **estilo)

        for origem, destino in dados["conexoes"]:
            fluxo.edge(origem, destino)

        img_bytes = fluxo.pipe(format="png")
        img_b64 = base64.b64encode(img_bytes).decode()

        html_img = f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
          <meta charset="UTF-8">
          <title>{dados.get("titulo", "Fluxograma")}</title>
          <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: auto;
                padding: 40px;
            }}
            header {{
                text-align: center;
                border-bottom: 1px solid #ccc;
                margin-bottom: 20px;
            }}
            header img {{
                height: 80px;
            }}
            h1, h2 {{
                margin: 5px;
            }}
            .fluxo-img {{
                max-height: 800px;
                width: auto;
                display: block;
                margin: auto;
                border: 1px solid #ccc;
                border-radius: 6px;
            }}
            .legenda {{
                font-size: 14px;
                margin-top: 20px;
            }}
            footer {{
                text-align: center;
                font-size: 11px;
                color: #888;
                margin-top: 30px;
                border-top: 1px solid #ccc;
                padding-top: 10px;
            }}
          </style>
        </head>
        <body>
          <header>
            <img src="cogex.png" alt="Logo COGEX"><br>
            <h1>CORREGEDORIA DO FORO EXTRAJUDICIAL</h1>
            <h2>{dados.get("titulo", "")}</h2>
          </header>
          <p><strong>Setor:</strong> {setor_escolhido}</p>
          <img src="data:image/png;base64,{img_b64}" alt="Fluxograma desenhado" class="fluxo-img">
          <div class="legenda">
            <h3>📘 Legenda</h3>
            ⬤ Início – `lightgreen`<br>
            ⬛ Tarefa – `lightblue`<br>
            ⬛ Verificação – `khaki`<br>
            ⬛ Publicação – `lightpink`<br>
            ⬛ Fiscalização – `lightgrey`<br>
            ⬤ Fim – `red`
          </div>
          <footer>
            Gerado automaticamente com desenho real – AppPy COGEX ©
          </footer>
        </body>
        </html>
        """

        nome_html = "fluxograma_com_imagem.html"
        with open(nome_html, "w", encoding="utf-8") as f:
            f.write(html_img)

        with open(nome_html, "rb") as f:
            st.download_button("📥 Baixar HTML com desenho real do fluxo", f, file_name=nome_html, mime="text/html")

except Exception as e:
    st.error(f"❌ Erro ao carregar ou renderizar o fluxo: {str(e)}")
