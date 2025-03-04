import pymupdf, os

output_dir = 'sample4'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

pdf_document = "sample4.pdf"

pdf = pymupdf.open(pdf_document)

print(f'original doc: {pdf}\nnum of pages: {pdf.page_count}\n\n{pdf.metadata}')

print(8*"\n")

blueprints_handler = dict()

for i in range(len(pdf)):
    page = pdf.load_page(i) 
    text = page.get_text("text").split('\n')
    try:
        mm = text.index("ММ")
    except:
        continue
    print(i+1, mm)
    code, name = text[mm+1:mm+3]
    # print(code, name)
    blueprints_handler.setdefault(code, [name]).append(i)

print(blueprints_handler)

for code, pages in blueprints_handler.items():

    blueprint_title = pages[0]

    pages_numbers = pages[1:]

    new_pdf = pymupdf.open()

    for page in pages_numbers:
        new_pdf.insert_pdf(pdf, from_page=page, to_page=page)
    
    output_filename = f'{output_dir}\{code} - {blueprint_title}.pdf'
    new_pdf.save(output_filename)
    new_pdf.close()

    print(f'Создан файл: {output_filename}')

pdf.close()