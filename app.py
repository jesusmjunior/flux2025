import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image
from datetime import datetime

st.set_page_config(page_title="COGEX – Modelagem de Processos", layout="centered")


# === Lista de setores da COGEX ===
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

# === Estilo A4 vertical ===
st.markdown("""
    <style>
    .main {
        max-width: 850px;
        margin: auto;
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# === Cabeçalho institucional ===
col_logo, col_texto = st.columns([1, 4])
with col_logo:
    if os.path.exists("cogex.png"):
        st.image(Image.open("cogex.png"), width=200)
with col_texto:
    st.markdown("### **COGEX - CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO**")
    st.markdown("##### Sistema de Modelagem de Processos")

st.divider()

# === Pesquisa e seleção de fluxogramas ===
st.markdown("### 📂 Selecione ou pesquise um fluxograma")
busca = st.text_input("🔍 Digite parte do nome do arquivo JSON:", "").lower()

# Filtragem dos arquivos JSON com base na busca
arquivos_json = sorted([f for f in os.listdir() if f.endswith(".json")])
arquivos_filtrados = [f for f in arquivos_json if busca in f.lower()]

if arquivos_filtrados:
    fluxo_selecionado = st.selectbox("📁 Arquivos Encontrados:", arquivos_filtrados)
else:
    st.warning("Nenhum arquivo JSON corresponde à busca.")
    st.stop()

# === Processamento do fluxo selecionado ===
try:
    with open(fluxo_selecionado, encoding='utf-8') as f:
        dados = json.load(f)

    if not all(key in dados for key in ["titulo", "etapas", "conexoes"]):
        st.error("O arquivo JSON selecionado não contém a estrutura necessária para um fluxograma.")
        st.stop()

    st.subheader(f"📌 {dados.get('titulo', 'Título não encontrado')}")
    setor_atual = dados.get("setor", setores_cogex[0])

    try:
        setor_index = setores_cogex.index(setor_atual)
    except ValueError:
        setor_index = 0
        st.warning(f"Setor '{setor_atual}' não encontrado na lista de setores COGEX. Selecionando o primeiro setor por padrão.")

    setor_escolhido = st.selectbox("🏛️ Setor:", setores_cogex, index=setor_index)

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

        for conexao in dados["conexoes"]:
            if len(conexao) >= 2:
                origem, destino = conexao[0], conexao[1]
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
    if st.button("📤 Exportar para HTML (modo A4 institucional com layout do app)"):
        tipo_cor = {key: key for key in estilo_map}
        html_export_visual = f"""
        <!DOCTYPE html>
        <html lang=\"pt-br\">
        <head>
          <meta charset=\"UTF-8\">
          <title>{dados['titulo']}</title>
          <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: auto; background: #fff; padding: 40px; color: #111; }}
            header {{ text-align: center; border-bottom: 1px solid #ccc; margin-bottom: 20px; }}
            header img {{ width: 120px; }}
            h1 {{ font-size: 20px; margin: 10px 0 0 0; }}
            h2 {{ font-size: 18px; color: #222; }}
            .setor {{ background: #f3f3f3; padding: 10px; margin-bottom: 20px; border-radius: 5px; }}
            .colunas {{ display: flex; gap: 30px; }}
            .col1 {{ flex: 2; }}
            .col2 {{ flex: 1; font-size: 14px; }}
            .box {{ padding: 10px; border-radius: 5px; margin-bottom: 15px; }}
            .inicio {{ background: lightgreen; }}
            .tarefa {{ background: lightblue; }}
            .verificacao {{ background: khaki; }}
            .publicacao {{ background: lightpink; }}
            .fiscalizacao {{ background: lightgrey; }}
            .fim {{ background: red; color: white; text-align: center; }}
            footer {{ text-align: center; font-size: 11px; color: #888; margin-top: 40px; border-top: 1px solid #ccc; padding-top: 10px; }}
          </style>
        </head>
        <body>
          <header>
            <img src=\"cogex.png\" alt=\"Logo COGEX\">
            <h1>CORREGEDORIA DO FORO EXTRAJUDICIAL</h1>
            <h2>{dados['titulo']}</h2>
          </header>
          <div class=\"setor\"><strong>Setor:</strong> {setor_escolhido}</div>
          <div class=\"colunas\">
            <div class=\"col1\">
        """
        for etapa in dados["etapas"]:
            classe = tipo_cor.get(etapa["tipo"], "tarefa")
            html_export_visual += f'<div class="box {classe}">{etapa["texto"].replace(chr(10), "<br>")}</div>\n'

        html_export_visual += f"""
            </div>
            <div class=\"col2\">
              <h3>📘 Legenda</h3>
              ⬤ <strong>Início</strong> – cor `lightgreen`<br>
              ⬛ <strong>Tarefa</strong> – cor `lightblue`<br>
              ⬛ <strong>Verificação</strong> – cor `khaki`<br>
              ⬛ <strong>Publicação</strong> – cor `lightpink`<br>
              ⬛ <strong>Fiscalização</strong> – cor `lightgrey`<br>
              ⬤ <strong>Fim</strong> – cor `red`<br>
              <hr>
              <h3>⚖️ Base Legal</h3>
              {dados.get("base_legal", "Não informada.")}
            </div>
          </div>
          <footer>
            Exportado automaticamente por AppPy-Cogex © - {datetime.now().strftime('%d/%m/%Y %H:%M')}
          </footer>
        </body>
        </html>
        """
        nome_base = os.path.splitext(fluxo_selecionado)[0]
        nome_html = f"{nome_base}_visual_exportado.html"
        with open(nome_html, "w", encoding="utf-8") as f:
            f.write(html_export_visual)

        with open(nome_html, "rb") as f:
            st.download_button("📥 Baixar HTML com layout institucional", f, file_name=nome_html, mime="text/html")

except Exception as e:
    st.error(f"❌ Erro ao carregar ou renderizar o fluxo: {str(e)}")
    # === Robô Flutuante Lateral ===
st.markdown("""
<div class="floating-robot">
    <div class=\"speech-bubble\"><a href=\"https://www.tjma.jus.br/atos/extrajudicial/geral/0/5657/pnao/provimentos-cogex" target=\"_blank\">Acesse COGEX</a></div>
    <img src=\"https://cdn-icons-png.flaticon.com/512/4712/4712035.png\" width="60">
    <div class="placa-jj">JJ I.A. COGEX</div>
</div>
""", unsafe_allow_html=True)

