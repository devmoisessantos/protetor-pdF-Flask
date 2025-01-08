import os
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import orange
from io import BytesIO


def modifier_pdf(file_path: str, cpf: str, position: str, color, upload_folder: str):
    try:
        # Inicia o canvas e cria um arquivo temporário em memória
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        width, height = A4

        text_width = can.stringWidth(cpf, "Helvetica", 12)
        x = width / 2 - text_width / 2  # Posição horizontal padrão (centrada)
        y = height / 2  # Posição vertical padrão (centrada)

        # Dicionário de posições possíveis
        positions = {
            'Esquerda': (50, height / 2),
            'Centro': (width / 2 - text_width / 2, height / 2),
            'Direita': (width - 50 - text_width, height / 2),
            'Cima': (width / 2 - text_width / 2, height - 50),
            'Baixo': (width / 2 - text_width / 2, 50),
            'Esquerda-Cima': (50, height - 50),
            'Esquerda-Baixo': (50, 50),
            'Centro-Cima': (width / 2 - text_width / 2, height - 50),
            'Centro-Baixo': (width / 2 - text_width / 2, 50),
            'Direita-Cima': (width - 50 - text_width, height - 50),
            'Direita-Baixo': (width - 50 - text_width, 50),
        }

        # Atribui a posição de acordo com o parâmetro 'position'
        # Se posição não encontrada, usa a padrão
        x, y = positions.get(position, (x, y))

        # Desenha o CPF na posição definida com a cor escolhida
        can.setFillColor(color)
        can.drawString(x, y, cpf)
        can.save()

        # Reinicia o ponteiro do pacote de BytesIO
        packet.seek(0)
        new_pdf = PdfReader(packet)

        # Abre o arquivo PDF existente
        existing_pdf = PdfReader(open(file_path, 'rb'))
        output = PdfWriter()

        # Mescla as páginas existentes com a página modificada
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            # Mescla a página gerada com a original
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)

        # Gera um nome único para o arquivo modificado
        modified_filename = f"modified_{os.path.basename(file_path)}"
        modified_filepath = os.path.join(upload_folder, modified_filename)

        # Salva o PDF modificado
        with open(modified_filepath, "wb") as output_stream:
            output.write(output_stream)

        print(
            f"PDF modificado com sucesso. Arquivo salvo em: {modified_filepath}")
        return modified_filepath

    except Exception as e:
        print(f"Erro durante a modificação do PDF: {str(e)}")
        raise e  # Levanta o erro para tratamento posterior
