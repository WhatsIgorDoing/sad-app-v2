from pathlib import Path

from docx import Document


def create_test_files():
    """Cria os arquivos de teste necessários."""

    # Garantir que o diretório existe
    fixtures_dir = Path("tests/fixtures")
    fixtures_dir.mkdir(parents=True, exist_ok=True)

    # Texto de teste
    test_text = "Relatório: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A"

    # Criar arquivo DOCX
    doc = Document()
    doc.add_paragraph(test_text)
    docx_path = fixtures_dir / "documento_rir.docx"
    doc.save(str(docx_path))
    print(f"✅ DOCX criado: {docx_path}")

    # Criar arquivo PDF usando PyPDF2 (mais simples)
    try:
        from reportlab.pdfgen import canvas

        pdf_path = fixtures_dir / "documento_rir.pdf"
        c = canvas.Canvas(str(pdf_path))
        c.drawString(100, 750, test_text)
        c.save()
        print(f"✅ PDF criado: {pdf_path}")
    except ImportError:
        # Se reportlab não estiver disponível, criar um arquivo texto que simula PDF
        pdf_path = fixtures_dir / "documento_rir.pdf"
        with open(pdf_path, "w", encoding="utf-8") as f:
            f.write("%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n")
            f.write("2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n")
            f.write(
                "3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/Contents 4 0 R\n>>\nendobj\n"
            )
            f.write(
                f"4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n"
                f"72 720 Td\n({test_text}) Tj\nET\nendstream\nendobj\n"
            )
            f.write(
                "xref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n"
                "0000000058 00000 n\n0000000115 00000 n\n"
                "0000000174 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\n"
                "startxref\n274\n%%EOF"
            )
        print(f"✅ PDF (simulado) criado: {pdf_path}")


if __name__ == "__main__":
    create_test_files()
