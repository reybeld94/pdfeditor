import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import io

class PDFProcessor:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_page_count(self):
        """Obtener número de páginas"""
        try:
            with open(self.filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return len(reader.pages)
        except Exception as e:
            print(f"Error al obtener número de páginas: {e}")
            raise Exception(f"No se pudo leer el archivo PDF: {str(e)}")

    def get_page_size(self, page_number):
        """Obtener tamaño de página"""
        try:
            with open(self.filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if page_number < len(reader.pages):
                    page = reader.pages[page_number]
                    return float(page.mediabox.width), float(page.mediabox.height)
                return 612, 792  # Tamaño letter por defecto
        except Exception as e:
            print(f"Error al obtener tamaño de página: {e}")
            return 612, 792  # Tamaño letter por defecto

    def add_text(self, page_number, text, x, y, font_size=12, color="#000000"):
        """Añadir texto a una página específica"""
        try:
            # Crear archivo temporal para el resultado
            temp_filepath = self.filepath + ".tmp"

            # Leer PDF original
            with open(self.filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                writer = PyPDF2.PdfWriter()

                # Crear overlay con texto
                overlay_buffer = self.create_text_overlay(text, x, y, font_size, color)
                overlay_reader = PyPDF2.PdfReader(overlay_buffer)

                # Procesar cada página
                for i, page in enumerate(reader.pages):
                    if i == page_number:
                        # Añadir overlay a la página especificada
                        page.merge_page(overlay_reader.pages[0])
                    writer.add_page(page)

                # Guardar en archivo temporal
                with open(temp_filepath, 'wb') as output_file:
                    writer.write(output_file)

            # Reemplazar archivo original con el temporal
            os.replace(temp_filepath, self.filepath)
            return True

        except Exception as e:
            print(f"Error al añadir texto: {e}")
            # Limpiar archivo temporal si existe
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            return False

    def create_text_overlay(self, text, x, y, font_size, color):
        """Crear overlay con texto"""
        buffer = io.BytesIO()

        # Crear canvas
        c = canvas.Canvas(buffer, pagesize=letter)

        # Configurar fuente y color
        c.setFont("Helvetica", font_size)

        # Convertir color hex a RGB
        if color.startswith('#'):
            color = color[1:]
        r = int(color[0:2], 16) / 255.0
        g = int(color[2:4], 16) / 255.0
        b = int(color[4:6], 16) / 255.0
        c.setFillColorRGB(r, g, b)

        # Ajustar coordenada Y (PDF tiene origen en la esquina inferior izquierda)
        page_height = 792  # Altura de página letter
        adjusted_y = page_height - y

        # Añadir texto
        c.drawString(x, adjusted_y, text)
        c.save()

        buffer.seek(0)
        return buffer

    def extract_text_from_page(self, page_number):
        """Extraer texto de una página"""
        try:
            with open(self.filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if page_number < len(reader.pages):
                    page = reader.pages[page_number]
                    return page.extract_text()
                return ""
        except Exception as e:
            print(f"Error al extraer texto: {e}")
            return ""

    def get_pdf_info(self):
        """Obtener información del PDF"""
        try:
            with open(self.filepath, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                return {
                    "pages": len(reader.pages),
                    "metadata": reader.metadata,
                    "size": os.path.getsize(self.filepath)
                }
        except Exception as e:
            print(f"Error al obtener info: {e}")
            return None