from fpdf import FPDF

# Gerar PDF institucional com layout A4 reduzido (70%)
pdf = FPDF(format='A4')
pdf.add_page()

# Títulos e cabeçalho institucional
pdf.set_font("Arial", 'B', 12)
pdf.cell(0, 8, "Corregedoria Geral do Foro Extrajudicial", ln=True, align='C')

pdf.set_font("Arial", 'B', 11)
pdf.cell(0, 8, "Processo Endógeno – Atualização Normativa (Provimento nº 33/2024)", ln=True, align='C')

pdf.set_font("Arial", '', 10)
pdf.cell(0, 6, "CGJ/MA – Coordenação de Normas (COGEX)", ln=True, align='C')

pdf.ln(8)

# Imagem centralizada e reduzida para 70% do espaço horizontal
page_width = 210  # A4 width in mm
margin = 15
img_width = (page_width - 2 * margin) * 0.7  # 70% of content width

pdf.image("/mnt/data/fluxograma_institucional.png", x=(page_width - img_width) / 2, w=img_width)

# Rodapé
pdf.set_y(-20)
pdf.set_font("Arial", 'I', 9)
pdf.cell(0, 10, "Documento gerado automaticamente por AppPy-Cogex ©", 0, 0, 'C')

# Exportar PDF
output_pdf_a4 = "/mnt/data/fluxograma_institucional_A4_reduzido.pdf"
pdf.output(output_pdf_a4)

output_pdf_a4
