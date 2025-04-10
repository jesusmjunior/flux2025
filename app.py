import streamlit as st
import base64

st.set_page_config(page_title="Exportação Fluxograma COGEX", layout="centered")

st.image("https://raw.githubusercontent.com/streamlit/streamlit-example/master/static/favicon.png", width=80)
st.markdown("## COGEX - CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO")
st.markdown("### Exportação de Fluxograma com Layout Completo")

st.markdown("---")

# Caminho da imagem incluída anteriormente
image_path = "image.png"  # Enviar para mesma pasta do app na nuvem

with open(image_path, "rb") as img_file:
    img_bytes = img_file.read()
    img_b64 = base64.b64encode(img_bytes).decode()

html_final = f'''
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Fluxograma COGEX</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      max-width: 850px;
      margin: auto;
      padding: 30px;
    }}
    .header {{
      text-align: center;
    }}
    .header img {{
      height: 80px;
      margin-bottom: 10px;
    }}
    .titulo {{
      font-size: 22px;
      font-weight: bold;
      margin-bottom: 10px;
    }}
    .subtitulo {{
      font-size: 16px;
      margin-bottom: 20px;
    }}
    .setor {{
      font-size: 14px;
      background: #f5f5f5;
      padding: 10px;
      font-weight: bold;
      border-radius: 5px;
    }}
    .fluxo-img {{
      margin: 30px auto;
      display: block;
      max-width: 100%;
      border-radius: 6px;
    }}
    .legenda, .legal {{
      margin-top: 30px;
      font-size: 14px;
    }}
    footer {{
      text-align: center;
      font-size: 11px;
      color: #888;
      margin-top: 40px;
      border-top: 1px solid #ccc;
      padding-top: 10px;
    }}
  </style>
</head>
<body>
  <div class="header">
    <img src="https://raw.githubusercontent.com/streamlit/streamlit-example/master/static/favicon.png">
    <div class="titulo">CORREGEDORIA DO FORO EXTRAJUDICIAL</div>
    <div class="subtitulo">Processo Endógeno – Atualização Normativa Institucional</div>
  </div>

  <div class="setor">Setor: Coordenadoria de Serventias Extrajudiciais</div>
  <img src="data:image/png;base64,{img_b64}" class="fluxo-img">

  <div class="legenda">
    <strong>📘 Legenda</strong><br>
    ⬤ Início – cor 'lightgreen'<br>
    ⬛ Tarefa – cor 'lightblue'<br>
    ⬛ Verificação – cor 'khaki'<br>
    ⬛ Publicação – cor 'lightpink'<br>
    ⬛ Fiscalização – cor 'lightgrey'<br>
    ⬤ Fim – cor 'red'
  </div>

  <div class="legal">
    <strong>⚖️ Base Legal</strong><br>
    Provimento nº 16/2022 + Resoluções CNJ + Temas STJ/STF 1.067 e 1.144
  </div>

  <footer>
    Sistema de Modelagem de Processos – COGEX/TJMA
  </footer>
</body>
</html>
'''

# Download HTML com layout institucional
st.download_button(
    label="📥 Baixar HTML com layout completo",
    data=html_final,
    file_name="fluxograma_visual_COGEX.html",
    mime="text/html"
)
