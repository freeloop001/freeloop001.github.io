# PDF 文件处理示例
# 需要安装: pip install pdfplumber PyPDF2
# 注意: 需要有实际的 PDF 文件才能运行

# 方法1: 使用 pdfplumber
try:
    import pdfplumber

    def read_pdf_plumber(filename):
        """使用 pdfplumber 读取 PDF"""
        with pdfplumber.open(filename) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                print(f"--- Page {i+1} ---")
                print(text[:500] if text else "No text")

except ImportError:
    print("pdfplumber 未安装: pip install pdfplumber")

# 方法2: 使用 PyPDF2
try:
    from PyPDF2 import PdfReader

    def read_pdf_pypdf2(filename):
        """使用 PyPDF2 读取 PDF"""
        reader = PdfReader(filename)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            print(f"--- Page {i+1} ---")
            print(text[:500] if text else "No text")

except ImportError:
    print("PyPDF2 未安装: pip install PyPDF2")

# 使用示例（需要实际的 PDF 文件）
# read_pdf_plumber("document.pdf")
# read_pdf_pypdf2("document.pdf")

print("PDF 处理示例完成，需要实际 PDF 文件才能运行")
