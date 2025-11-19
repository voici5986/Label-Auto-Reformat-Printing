from PIL import Image
import fitz  # PyMuPDF


class PDFService:
    def __init__(self):
        pass

    def tile_label_image_to_pdf(self, image_path: str, output_pdf: str, rows: int,
                                cols: int, margin_mm: int, spacing_mm: int, orientation: str,
                                error_label_size_msg: str) -> None:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.units import mm

        # 输入参数验证
        if rows <= 0 or cols <= 0:
            raise ValueError("行数和列数必须大于0")
        if margin_mm < 0 or spacing_mm < 0:
            raise ValueError("边距和间距不能为负数")
        if orientation not in ['landscape', 'portrait']:
            raise ValueError("方向必须是 'landscape' 或 'portrait'")

        if orientation == 'landscape':
            page_size = landscape(A4)
        else:
            page_size = A4

        page_width, page_height = page_size
        margin = margin_mm * mm
        spacing = spacing_mm * mm

        usable_width = page_width - 2 * margin
        usable_height = page_height - 2 * margin

        label_width = (usable_width - (cols - 1) * spacing) / cols
        label_height = (usable_height - (rows - 1) * spacing) / rows

        if label_width <= 0 or label_height <= 0:
            raise ValueError(error_label_size_msg)

        # 直接抛出原始异常，让调用层处理
        img = Image.open(image_path)
        img.load()

        c = canvas.Canvas(output_pdf, pagesize=page_size)

        for row in range(rows):
            for col in range(cols):
                x = margin + col * (label_width + spacing)
                y = page_height - margin - (row + 1) * label_height - row * spacing
                c.drawImage(
                    image_path,
                    x,
                    y,
                    width=label_width,
                    height=label_height,
                    preserveAspectRatio=True,
                )

        c.save()

    def pdf_to_pixmap(self, pdf_path: str, zoom: float = 3.0) -> "QPixmap":
        document = fitz.open(pdf_path)
        try:
            page = document[0]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            from PyQt6.QtGui import QPixmap

            img_data = pix.tobytes("png")
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            return pixmap
        finally:
            document.close()

    def pdf_to_png(self, pdf_path: str, png_path: str, dpi: int = 300) -> None:
        zoom = dpi / 72
        document = fitz.open(pdf_path)
        try:
            page = document[0]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            pix.save(png_path)
        finally:
            document.close()
