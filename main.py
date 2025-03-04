from PyPDF2 import PdfReader

pdf_document = "sample.pdf"

with open(pdf_document, "rb") as file:
    pdf = PdfReader(file, strict=False)

    page = pdf.pages[0]
    print(f'page: 1\nmeta: {page}\nValue:\n\n{page.extract_text()}')