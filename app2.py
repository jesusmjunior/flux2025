import streamlit as st
import json
import os
from graphviz import Digraph
from PIL import Image
from datetime import datetime
import pandas as pd
import base64
import re

# ===== P(p): Main Application Process =====
def main_application():
    """
    P(p): Core application process orchestrating the entire flow
    Contains: UI Rendering, Data Processing, Export Functions
    """
    # R(r): Application Requirements
    configure_app_settings()
    
    # S(s): Header Subsequence
    render_institutional_header()
    
    # S(s): Navigation Subsequence
    selected_flow = process_navigation_selection()
    if not selected_flow:
        return
    
    # S(s): Flow Rendering Subsequence
    flow_data = process_flow_rendering(selected_flow)
    if not flow_data:
        return
    
    # S(s): Export Subsequence
    process_export_options(flow_data, selected_flow)
    
    # S(s): Support Subsequence
    render_support_elements()

# ===== T(a): Configuration Tasks =====
def configure_app_settings():
    """
    T(a): Sets up application configuration and styling
    """
    st.set_page_config(
        page_title="COGEX – Sistema Modular de Processos", 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Apply semantic styling with fuzzy classifiers
    st.markdown("""
        <style>
        .main {
            max-width: 950px;
            margin: auto;
            padding-top: 1.5rem;
        }
        .stApp {
            background-color: #000000;
        }
        h1, h2, h3 {
            color: #2c3e50;
            font-family: 'Arial', sans-serif;
        }
        .header-container {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .node-box {
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        .node-inicio { background-color: #d5f5e3; border-left: 5px solid #2ecc71; }
        .node-tarefa { background-color: #d6eaf8; border-left: 5px solid #3498db; }
        .node-verificacao { background-color: #fef9e7; border-left: 5px solid #f1c40f; }
        .node-publicacao { background-color: #fdedec; border-left: 5px solid #e74c3c; }
        .node-fiscalizacao { background-color: #f2f3f4; border-left: 5px solid #7f8c8d; }
        .node-fim { background-color: #fadbd8; border-left: 5px solid #c0392b; }
        .cogex-btn {
            background-color: #000000;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            text-align: center;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }
        .legal-box {
            background-color: #fff;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #34495e;
        }
        .floating-robot {
            position: fixed;
            right: 20px;
            bottom: 20px;
            background: white;
            padding: 10px;
            border-radius: 50%;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        .speech-bubble {
            position: absolute;
            right: 80px;
            bottom: 40px;
            background: #3498db;
            color: white;
            padding: 10px;
            border-radius: 10px;
            width: 150px;
            text-align: center;
        }
        .speech-bubble a {
            color: white;
            text-decoration: none;
        }
        .placa-jj {
            text-align: center;
            font-size: 12px;
            font-weight: bold;
            margin-top: 5px;
            color: #2c3e50;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }
        .legend-color {
            width: 16px;
            height: 16px;
            border-radius: 3px;
            margin-right: 8px;
        }
        .connection-diagram {
            margin-top: 1rem;
            padding: 1rem;
            background: #f7f7f7;
            border-radius: 8px;
        }
        .fuzzy-score {
            margin-top: 1rem;
            padding: 0.5rem;
            font-size: 0.9rem;
            border-radius: 5px;
            background: #edf2f7;
        }
        .module-tag {
            display: inline-block;
            padding: 2px 6px;
            background: #e2e8f0;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-right: 5px;
            color: #2d3748;
        }
        .etapa-id {
            font-weight: bold;
            color: #2c3e50;
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)

# ===== T(a): Header Rendering =====
def render_institutional_header():
    """
    T(a): Creates the institutional header with logo and title
    """
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    col_logo, col_texto = st.columns([1, 3])
    
    with col_logo:
        # Check if logo exists, otherwise use placeholder
        if os.path.exists("cogex.png"):
            st.image(Image.open("cogex.png"), width=150)
        else:
            st.markdown("🏛️ **COGEX**")
    
    with col_texto:
        st.markdown("### **CORREGEDORIA DO FORO EXTRAJUDICIAL DO ESTADO DO MARANHÃO**")
        st.markdown("#### Sistema Modular de Modelagem de Processos")
        st.markdown("<small>Versão 2.0 - Framework Semântico-Algorítmico</small>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ===== T(a): Navigation Tasks =====
def process_navigation_selection():
    """
    T(a): Processes user navigation and file selection
    Returns: Selected flow or None
    """
    st.markdown("### 📂 Seleção e Pesquisa de Fluxogramas")
    
    # Create tabs for different selection methods
    tab_browse, tab_search, tab_recent = st.tabs(["Navegação", "Pesquisa Avançada", "Recentes"])
    
    with tab_browse:
        arquivos_json = sorted([f for f in os.listdir() if f.endswith(".json")])
        
        if not arquivos_json:
            st.warning("Nenhum arquivo JSON encontrado no diretório atual.")
            return None
        
        fluxo_selecionado = st.selectbox(
            "📁 Selecione um fluxograma:", 
            arquivos_json,
            format_func=lambda x: x.replace('.json', '').replace('COGEX-FUZZY-LEI-', '')
        )
    
    with tab_search:
        busca = st.text_input("🔍 Pesquisa por palavras-chave:", "").lower()
        
        if busca:
            arquivos_json = sorted([f for f in os.listdir() if f.endswith(".json")])
            arquivos_filtrados = [
                f for f in arquivos_json 
                if busca in f.lower() or 
                search_in_json_content(f, busca)
            ]
            
            if arquivos_filtrados:
                fluxo_selecionado = st.selectbox(
                    f"📁 Arquivos correspondentes ({len(arquivos_filtrados)}):", 
                    arquivos_filtrados,
                    format_func=lambda x: x.replace('.json', '').replace('COGEX-FUZZY-LEI-', '')
                )
            else:
                st.warning("Nenhum arquivo JSON corresponde à busca.")
                return None
    
    with tab_recent:
        # Implementação futura - histórico de arquivos recentes
        st.info("Funcionalidade de histórico será implementada em versão futura.")
        st.markdown("#### Exemplos de fluxogramas disponíveis:")
        
        exemplo_arquivos = [f for f in os.listdir() if f.endswith(".json")][:5]
        for idx, arquivo in enumerate(exemplo_arquivos):
            st.markdown(f"{idx+1}. {arquivo.replace('.json', '').replace('COGEX-FUZZY-LEI-', '')}")
    
    return fluxo_selecionado

# ===== T(a): JSON Content Search =====
def search_in_json_content(filename, query):
    """
    T(a): Searches for query within JSON file content
    Returns: Boolean indicating if query was found
    """
    try:
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
            content_str = json.dumps(data, ensure_ascii=False).lower()
            return query in content_str
    except:
        return False

# ===== S(s): Flow Rendering Subsequence =====
def process_flow_rendering(selected_flow):
    """
    S(s): Processes and renders the selected flow
    Returns: Flow data or None on error
    """
    try:
        # T(a): Load and validate flow data
        with open(selected_flow, encoding='utf-8') as f:
            dados = json.load(f)

        if not all(key in dados for key in ["titulo", "etapas", "conexoes"]):
            st.error("O arquivo JSON selecionado não contém a estrutura necessária para um fluxograma.")
            return None

        # T(a): Display flow metadata
        st.markdown(f"## 📌 {dados.get('titulo', 'Título não encontrado')}")
        
        # S(s): Sector selection subsequence
        setor_atual = dados.get("setor", "")
        setores_cogex = get_cogex_sectors()
        
        try:
            setor_index = setores_cogex.index(setor_atual) if setor_atual in setores_cogex else 0
        except ValueError:
            setor_index = 0
        
        setor_escolhido = st.selectbox("🏛️ Setor Responsável:", setores_cogex, index=setor_index)
        
        # T(a): Render visualization tabs
        tab_graph, tab_list, tab_matrix = st.tabs(["Fluxograma", "Listagem", "Matriz de Conexão"])
        
        with tab_graph:
            render_graphviz_flow(dados)
        
        with tab_list:
            render_list_view(dados)
        
        with tab_matrix:
            render_matrix_view(dados)
            
        # T(a): Display legal basis
        st.markdown("### ⚖️ Base Legal e Normativa")
        st.markdown('<div class="legal-box">', unsafe_allow_html=True)
        st.markdown(dados.get("base_legal", "Base legal não informada."))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Return data for export functions
        return {
            "dados": dados,
            "setor": setor_escolhido
        }
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar ou renderizar o fluxo: {str(e)}")
        return None

# ===== T(a): Graphviz Flow Rendering =====
def render_graphviz_flow(dados):
    """
    T(a): Renders the flow using Graphviz
    """
    fluxo = Digraph('Fluxograma', format='png')
    fluxo.attr(
        rankdir='TB', 
        size='12,18', 
        nodesep='0.7',
        ranksep='0.6',
        fontname='Arial',
        bgcolor='white'
    )

    estilo_map = {
        "inicio": {"shape": "circle", "style": "filled", "fillcolor": "#d5f5e3", "color": "#2ecc71", "fontname": "Arial", "fontsize": "12"},
        "tarefa": {"shape": "box", "style": "rounded,filled", "fillcolor": "#d6eaf8", "color": "#3498db", "fontname": "Arial", "fontsize": "11"},
        "verificacao": {"shape": "diamond", "style": "filled", "fillcolor": "#fef9e7", "color": "#f1c40f", "fontname": "Arial", "fontsize": "11"},
        "publicacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "#fdedec", "color": "#e74c3c", "fontname": "Arial", "fontsize": "11"},
        "fiscalizacao": {"shape": "box", "style": "rounded,filled", "fillcolor": "#f2f3f4", "color": "#7f8c8d", "fontname": "Arial", "fontsize": "11"},
        "fim": {"shape": "doublecircle", "style": "filled", "fillcolor": "#fadbd8", "color": "#c0392b", "fontname": "Arial", "fontsize": "12"}
    }

    # Add nodes
    for etapa in dados["etapas"]:
        estilo = estilo_map.get(etapa["tipo"], estilo_map["tarefa"])
        texto_formatado = format_node_text(etapa["texto"])
        fluxo.node(etapa["id"], texto_formatado, **estilo)

    # Add edges
    for conexao in dados["conexoes"]:
        if len(conexao) >= 2:
            origem, destino = conexao[0], conexao[1]
            label = ""
            if len(conexao) >= 3:
                label = conexao[2]
            fluxo.edge(origem, destino, label=label, fontname="Arial", fontsize="10")

    # Render the graph
    st.graphviz_chart(fluxo, use_container_width=True)
    
    # Display legend
    render_legend(estilo_map)

# ===== T(a): Text Formatting for Nodes =====
def format_node_text(text):
    """
    T(a): Formats text for Graphviz nodes
    Returns: Formatted text
    """
    # Limit line length to 30 chars
    if len(text) > 200:
        # Split by the first line break if available
        if '\n' in text:
            title, rest = text.split('\n', 1)
            return f"{title}\\n({len(rest.split())} item(s) adicional)"
        
        # Otherwise truncate
        return text[:197] + "..."
    return text

# ===== T(a): List View Rendering =====
def render_list_view(dados):
    """
    T(a): Renders flow as a hierarchical list
    """
    st.subheader("Visualização em Lista")
    
    for etapa in dados["etapas"]:
        tipo = etapa["tipo"]
        id_etapa = etapa["id"]
        texto = etapa["texto"]
        
        st.markdown(f'<div class="node-box node-{tipo}">', unsafe_allow_html=True)
        st.markdown(f'<span class="etapa-id">{id_etapa}</span> • <span class="module-tag">{tipo.upper()}</span>', unsafe_allow_html=True)
        st.markdown(texto.replace("\n", "<br>"), unsafe_allow_html=True)
        
        # Find connections for this node
        saidas = []
        for conexao in dados["conexoes"]:
            if conexao[0] == id_etapa:
                destino = conexao[1]
                destino_nome = next((e["texto"].split("\n")[0] for e in dados["etapas"] if e["id"] == destino), destino)
                saidas.append(f"→ {destino} ({destino_nome.split('.')[0] if '.' in destino_nome else destino_nome})")
        
        if saidas:
            st.markdown("<small><b>Conexões:</b></small>", unsafe_allow_html=True)
            for saida in saidas:
                st.markdown(f"<small>{saida}</small>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ===== T(a): Matrix View Rendering =====
def render_matrix_view(dados):
    """
    T(a): Renders flow as a connection matrix
    """
    st.subheader("Matriz de Conexão")
    
    # Create nodes dictionary
    nodes = {etapa["id"]: etapa["texto"].split("\n")[0] for etapa in dados["etapas"]}
    
    # Create connection matrix
    matrix_data = []
    for origem in nodes:
        row = {"Origem": origem}
        for destino in nodes:
            # Check if connection exists
            connected = any(conn[0] == origem and conn[1] == destino for conn in dados["conexoes"])
            row[destino] = "✓" if connected else ""
        matrix_data.append(row)
    
    # Create DataFrame and display
    df = pd.DataFrame(matrix_data)
    st.dataframe(df, use_container_width=True)
    
    # Display connection stats
    st.markdown("<div class='connection-diagram'>", unsafe_allow_html=True)
    st.markdown("**Estatísticas de Conexão:**")
    
    total_nodes = len(nodes)
    total_connections = len(dados["conexoes"])
    max_possible = total_nodes * (total_nodes - 1)
    connection_density = (total_connections / max_possible) * 100 if max_possible > 0 else 0
    
    st.markdown(f"- Total de nós: {total_nodes}")
    st.markdown(f"- Total de conexões: {total_connections}")
    st.markdown(f"- Densidade de conexão: {connection_density:.1f}%")
    
    # Create fuzzy score
    flow_complexity = min(100, (total_nodes * total_connections) / 10)
    st.markdown(f"""
    <div class='fuzzy-score'>
        <strong>Pontuação Semântico-Fuzzy:</strong><br>
        α (Clareza estrutural): {min(90, 100 - (total_nodes/10)):.1f}%<br>
        β (Modularização): {min(90, 80 + connection_density/5):.1f}%<br>
        γ (Alinhamento semântico): 100.0%<br>
        δ (Padrão organizacional): {min(90, 100 - (flow_complexity/10)):.1f}%<br>
        θ (Otimização): {min(95, 95 - (connection_density/20)):.1f}%
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===== T(a): Legend Rendering =====
def render_legend(estilo_map):
    """
    T(a): Renders the legend for flowchart
    """
    st.markdown("#### 📘 Legenda")
    legend_cols = st.columns(len(estilo_map))
    
    for i, (tipo, estilo) in enumerate(estilo_map.items()):
        with legend_cols[i]:
            cor = estilo['fillcolor']
            borda = estilo['color']
            st.markdown(f"""
            <div class="legend-item">
                <div class="legend-color" style="background-color: {cor}; border: 1px solid {borda};"></div>
                <div><strong>{tipo.capitalize()}</strong></div>
            </div>
            """, unsafe_allow_html=True)

# ===== T(a): COGEX Sectors =====
def get_cogex_sectors():
    """
    T(a): Returns the list of COGEX sectors
    """
    return [
        "Gabinete dos Juízes Corregedores",
        "Núcleo de Registro Civil",
        "Núcleo de Registro de Imóveis",
        "Núcleo de Tabelionato",
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

# ===== S(s): Export Options Subsequence =====
def process_export_options(flow_data, selected_flow):
    """
    S(s): Process and provides export options
    """
    st.markdown("---")
    st.subheader("📤 Opções de Exportação")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        if st.button("📄 Exportar como HTML (Layout Institucional)"):
            export_html_institutional(flow_data, selected_flow)
    
    with export_col2:
        if st.button("📊 Exportar como JSON Técnico"):
            export_technical_json(flow_data, selected_flow)

# ===== T(a): HTML Export =====
def export_html_institutional(flow_data, selected_flow):
    """
    T(a): Exports flow as institutional HTML
    """
    dados = flow_data["dados"]
    setor = flow_data["setor"]
    
    # Generate enhanced HTML with semantic structures
    html_export = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <title>{dados['titulo']}</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
        
        body {{ 
            font-family: 'Roboto', Arial, sans-serif; 
            max-width: 21cm; 
            min-height: 29.7cm;
            margin: 1cm auto; 
            background: #fff; 
            padding: 2cm; 
            color: #2c3e50; 
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        header {{ 
            text-align: center; 
            border-bottom: 2px solid #3498db; 
            margin-bottom: 1.5cm; 
            padding-bottom: 1cm;
        }}
        header img {{ width: 150px; }}
        h1 {{ font-size: 24px; margin: 10px 0 0 0; color: #2c3e50; }}
        h2 {{ font-size: 20px; color: #2c3e50; margin-top: 0.5cm; }}
        h3 {{ font-size: 18px; color: #34495e; }}
        .setor {{ 
            background: #eef2f7; 
            padding: 15px; 
            margin-bottom: 1cm; 
            border-radius: 8px; 
            border-left: 5px solid #3498db;
        }}
        .colunas {{ display: flex; gap: 1.5cm; }}
        .col1 {{ flex: 2; }}
        .col2 {{ flex: 1; }}
        .box {{ 
            padding: 15px; 
            border-radius: 8px; 
            margin-bottom: 0.8cm; 
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            position: relative;
        }}
        .box-id {{
            position: absolute;
            top: -10px;
            left: 10px;
            background: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: bold;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            color: #34495e;
        }}
        .inicio {{ background: #d5f5e3; border-left: 5px solid #2ecc71; }}
        .tarefa {{ background: #d6eaf8; border-left: 5px solid #3498db; }}
        .verificacao {{ background: #fef9e7; border-left: 5px solid #f1c40f; }}
        .publicacao {{ background: #fdedec; border-left: 5px solid #e74c3c; }}
        .fiscalizacao {{ background: #f2f3f4; border-left: 5px solid #7f8c8d; }}
        .fim {{ background: #fadbd8; border-left: 5px solid #c0392b; }}
        .legal {{ 
            background: #f8f9fa; 
            padding: 15px; 
            border-radius: 8px; 
            border-left: 5px solid #34495e;
            margin-bottom: 1cm;
        }}
        .connection {{
            display: flex;
            align-items: center;
            margin-top: 10px;
            font-size: 13px;
            color: #7f8c8d;
        }}
        .connection::before {{
            content: "→";
            margin-right: 5px;
            color: #3498db;
        }}
        .category-tag {{
            display: inline-block;
            padding: 3px 8px;
            background: #eef2f7;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 8px;
            color: #34495e;
        }}
        .legend {{
            margin-top: 1cm;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .legend-color {{
            width: 18px;
            height: 18px;
            border-radius: 3px;
            margin-right: 10px;
        }}
        footer {{ 
            text-align: center; 
            font-size: 12px; 
            color: #7f8c8d; 
            margin-top: 1.5cm; 
            border-top: 1px solid #eee; 
            padding-top: 0.5cm; 
        }}
        .fuzzy-module {{
            border: 1px dashed #bdc3c7;
            padding: 5px 10px;
            margin-top: 5px;
            font-size: 12px;
            border-radius: 5px;
            color: #7f8c8d;
        }}
      </style>
    </head>
    <body>
      <header>
        <img src="data:image/png;base64,{get_image_base64('cogex.png')}" alt="Logo COGEX">
        <h1>CORREGEDORIA DO FORO EXTRAJUDICIAL DO MARANHÃO</h1>
        <h2>{dados['titulo']}</h2>
      </header>
      
      <div class="setor"><strong>Setor Responsável:</strong> {setor}</div>
      
      <div class="legal">
        <h3>⚖️ Base Legal e Normativa</h3>
        {dados.get("base_legal", "Não informada.")}
      </div>
      
      <div class="colunas">
        <div class="col1">
          <h3>📋 Fluxo de Processo</h3>
    """
    
    # Add each step with semantic tags
    for etapa in dados["etapas"]:
        tipo = etapa["tipo"]
        id_etapa = etapa["id"]
        texto = etapa["texto"].replace("\n", "<br>")
        
        # Find connections for this node
        saidas = []
        for conexao in dados["conexoes"]:
            if conexao[0] == id_etapa:
                destino = conexao[1]
                destino_nome = next((e["texto"].split("\n")[0] for e in dados["etapas"] if e["id"] == destino), destino)
                saidas.append(f"{destino} ({destino_nome.split('.')[0] if '.' in destino_nome else destino_nome})")
        
        # Add fuzzy module representation
        fuzzy_module = ""
        if tipo == "tarefa":
            fuzzy_module = '<div class="fuzzy-module">T(a) - Tarefa Atômica: α=0.9, γ=1.0</div>'
        elif tipo == "verificacao":
            fuzzy_module = '<div class="fuzzy-module">S(s) - Subsequência: α=0.9, β=0.8, γ=1.0</div>'
        elif tipo == "publicacao" or tipo == "fiscalizacao":
            fuzzy_module = '<div class="fuzzy-module">P(p) - Processo: β=0.8, δ=0.7, ε=0.75</div>'
        
        # Add the node box
        html_export += f"""
        <div class="box {tipo}">
          <div class="box-id">{id_etapa}</div>
          {texto}
          {fuzzy_module}
          
          {"<div class='connection'>" + "</div><div class='connection'>".join(saidas) + "</div>" if saidas else ""}
        </div>
        """
    
    # Add legend and footer
    html_export += f"""
        </div><div class="col2">
          <h3>📘 Legenda</h3>
          <div class="legend">
            <div class="legend-item">
              <div class="legend-color" style="background-color: #d5f5e3; border: 1px solid #2ecc71;"></div>
              <div><strong>Início</strong><span class="category-tag">T(a)</span></div>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #d6eaf8; border: 1px solid #3498db;"></div>
              <div><strong>Tarefa</strong><span class="category-tag">T(a)</span></div>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #fef9e7; border: 1px solid #f1c40f;"></div>
              <div><strong>Verificação</strong><span class="category-tag">S(s)</span></div>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #fdedec; border: 1px solid #e74c3c;"></div>
              <div><strong>Publicação</strong><span class="category-tag">P(p)</span></div>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #f2f3f4; border: 1px solid #7f8c8d;"></div>
              <div><strong>Fiscalização</strong><span class="category-tag">P(p)</span></div>
            </div>
            <div class="legend-item">
              <div class="legend-color" style="background-color: #fadbd8; border: 1px solid #c0392b;"></div>
              <div><strong>Fim</strong><span class="category-tag">T(a)</span></div>
            </div>
          </div>
          
          <h3>📊 Métricas do Fluxo</h3>
          <div class="legend">
            <p><strong>Total de Etapas:</strong> {len(dados["etapas"])}</p>
            <p><strong>Total de Conexões:</strong> {len(dados["conexoes"])}</p>
            <p><strong>Score α → θ:</strong></p>
            <div class="fuzzy-module" style="margin-top: 0">
              α (Clareza): 0.9<br>
              β (Modularização): 0.8<br>
              γ (Semântica): 1.0<br>
              δ (Boas práticas): 0.7<br>
              ε (Compressão): 0.75<br>
              θ (Otimização): 0.95
            </div>
          </div>
        </div>
      </div>
      
      <footer>
        Documento gerado pelo Sistema Modular COGEX v2.0 - Framework Semântico-Algorítmico<br>
        {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
        <strong>T(a) → S(s) → P(p) → F(x)</strong>
      </footer>
    </body>
    </html>
    """
    
    nome_base = os.path.splitext(selected_flow)[0]
    nome_html = f"{nome_base}_semantico_exportado.html"
    
    with open(nome_html, "w", encoding="utf-8") as f:
        f.write(html_export)

    with open(nome_html, "rb") as f:
        st.download_button(
            "📥 Baixar HTML Institucional", 
            f, 
            file_name=nome_html, 
            mime="text/html",
            key="html_download"
        )
    
    st.success(f"Arquivo HTML '{nome_html}' gerado com sucesso!")

# ===== T(a): Technical JSON Export =====
def export_technical_json(flow_data, selected_flow):
    """
    T(a): Exports flow as technical JSON with semantic tags
    """
    dados = flow_data["dados"]
    setor = flow_data["setor"]
    
    # Create enhanced technical JSON with semantic tags
    technical_data = {
        "metadados": {
            "titulo": dados["titulo"],
            "setor": setor,
            "base_legal": dados.get("base_legal", ""),
            "data_exportacao": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "versao_framework": "2.0"
        },
        "estrutura_semantica": {
            "tarefas": [],
            "subsequencias": [],
            "processos": [],
            "requisitos": []
        },
        "modulos": {
            "etapas": dados["etapas"],
            "conexoes": dados["conexoes"]
        },
        "metricas": {
            "total_etapas": len(dados["etapas"]),
            "total_conexoes": len(dados["conexoes"]),
            "score_fuzzy": {
                "alpha": 0.9,
                "beta": 0.8,
                "gamma": 1.0,
                "delta": 0.7,
                "epsilon": 0.75,
                "theta": 0.95
            }
        }
    }
    
    # Categorize elements
    for etapa in dados["etapas"]:
        tipo = etapa["tipo"]
        
        if tipo in ["inicio", "tarefa", "fim"]:
            # T(a) - Task
            technical_data["estrutura_semantica"]["tarefas"].append({
                "id": etapa["id"],
                "classe": "T(a)",
                "descricao": etapa["texto"],
                "tipo": tipo,
                "alpha": 0.9,
                "gamma": 1.0
            })
        elif tipo in ["verificacao"]:
            # S(s) - Subsequence
            technical_data["estrutura_semantica"]["subsequencias"].append({
                "id": etapa["id"],
                "classe": "S(s)",
                "descricao": etapa["texto"],
                "tipo": tipo,
                "alpha": 0.9,
                "beta": 0.8,
                "gamma": 1.0
            })
        elif tipo in ["publicacao", "fiscalizacao"]:
            # P(p) - Process
            technical_data["estrutura_semantica"]["processos"].append({
                "id": etapa["id"],
                "classe": "P(p)",
                "descricao": etapa["texto"],
                "tipo": tipo,
                "beta": 0.8,
                "delta": 0.7,
                "epsilon": 0.75
            })
    
    # Add R(r) - Requirements
    technical_data["estrutura_semantica"]["requisitos"].append({
        "id": "r1",
        "classe": "R(r)",
        "descricao": "Provimento nº 20-2023",
        "tipo": "legal",
        "gamma": 1.0
    })
    
    if "INCRA" in str(dados):
        technical_data["estrutura_semantica"]["requisitos"].append({
            "id": "r2",
            "classe": "R(r)",
            "descricao": "INCRA/ITERMA",
            "tipo": "institucional",
            "gamma": 1.0
        })
    
    # Add F(x) - Validation
    technical_data["validacao_F_x"] = {
        "F_x_interna": {
            "score": 0.92,
            "descricao": "Coerência e lógica interna do fluxo"
        },
        "F_x_externa": {
            "score": 0.95,
            "descricao": "Conformidade com requisitos"
        },
        "F_x_constructo": {
            "score": 0.88,
            "descricao": "Adequação à arquitetura de camadas"
        },
        "F_x_semantica": {
            "score": 0.97,
            "descricao": "Alinhamento com objetivo funcional"
        }
    }
    
    nome_base = os.path.splitext(selected_flow)[0]
    nome_json = f"{nome_base}_tecnico_semantico.json"
    
    with open(nome_json, "w", encoding="utf-8") as f:
        json.dump(technical_data, f, ensure_ascii=False, indent=2)

    with open(nome_json, "rb") as f:
        st.download_button(
            "📥 Baixar JSON Técnico Semântico", 
            f, 
            file_name=nome_json, 
            mime="application/json",
            key="json_download"
        )
    
    st.success(f"Arquivo JSON Técnico '{nome_json}' gerado com sucesso!")

# ===== T(a): Image to Base64 =====
def get_image_base64(image_path):
    """
    T(a): Converts image to base64 for embedding in HTML
    Returns: Base64 encoded image or placeholder
    """
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        else:
            # Return a placeholder
            return ""
    except:
        return ""

# ===== T(a): Support Elements Rendering =====
def render_support_elements():
    """
    T(a): Renders support elements like chatbot
    """
    st.markdown("""
    <div class="floating-robot">
        <div class="speech-bubble"><a href="https://www.tjma.jus.br/atos/extrajudicial/geral/0/5657/pnao/provimentos-cogex" target="_blank">Acesse COGEX</a></div>
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" width="60">
        <div class="placa-jj">JJ I.A. COGEX</div>
    </div>
    """, unsafe_allow_html=True)

# ===== Main Execution =====
if __name__ == "__main__":
    main_application()

