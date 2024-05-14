# Ler uma lista de pdfs
# Salvar os pdfs em arquivos txt para leitura
# # depois de criar o arquivo txt deletar o pdf.

# # PROCURAR -> [SEGURADORA, SEGURADO, PROPOSTA, APÓLICE, ENDOSSO,
# ITEM, PLACA, PREMIO LÍQUIDO, PREMIO TOTAL, RAMO, VENCIMENTO DAS PARCELAS
# , QUANTIDADE DE PARCELAS]
from pdfminer.high_level import extract_text
import os

# Procura os pdfs e cria uma lista
files = []
for i in os.listdir(r"/home/petala/Documents/projetos/boomer_pdf_scraping/input_pdfs"):
    path_folder = "input_pdfs/"
    path = f"{path_folder}{i}"
    files.append(path)
    print(files)

# Extrai o texto dos pdfs em um txt
for file in files:
    text = extract_text(file)
    print(text)
    with open("Output.txt", "w") as text_file:
        text_file.write(text)


path = "Output.txt"
file = open(path)

print(file.readline())
file.close()
