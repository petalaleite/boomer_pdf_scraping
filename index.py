import re

from pdfminer.high_level import extract_pages, extract_text

# nota: objetivo adicionar lista de pdfs
pdf_path = "boomer_sample.pdf"
# parse pdf to text
text = extract_text(pdf_path)

# write text to txt file


def write_text_file(text):
    with open("Output.txt", "w") as text_file:
        text_file.write(text)


# # PROCURAR -> [SEGURADORA, SEGURADO, PROPOSTA, APÓLICE, ENDOSSO, ITEM, PLACA, PREMIO LÍQUIDO, PREMIO TOTAL, RAMO, VENCIMENTO DAS PARCELAS, QUANTIDADE DE PARCELAS]
print(matches)
