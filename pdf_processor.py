from pymupdf import open as pdfopen
from os import path, makedirs

def process_pdf(input_file, output_dir, progress_callback=None):

    if not path.exists(output_dir):
        makedirs(output_dir)

    try:
        pdf = pdfopen(input_file)
    except Exception as e:
        raise Exception(f'Ошибка открытия PDF: {e}')
    
    blueprints_handler = dict()
    total_pages = len(pdf)

    for i in range(total_pages):
        page = pdf.load_page(i)
        text = page.get_text("text").split('\n')
        try:
            mm = text.index('ММ')
        except ValueError:
            continue
        code, name = text[mm+1:mm+3]
        blueprints_handler.setdefault(code, [name]).append(i)

        if progress_callback:
            progress_callback((i+1)/total_pages * 100)

    total_blueprints = len(blueprints_handler)
    i = 0

    for code, pages in blueprints_handler.items():
        blueprint_title = pages[0]
        page_numbers = pages[1:]

        new_pdf = pdfopen()

        for page in page_numbers:
            new_pdf.insert_pdf(pdf, from_page=page, to_page=page)
        
        output_filename = path.join(output_dir, f"{code} - {blueprint_title}.pdf")
        new_pdf.save(output_filename)
        new_pdf.close()

        if progress_callback:
            progress_callback((i+1)/total_blueprints * 100)
            i += 1
    
    pdf.close()

