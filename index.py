import pymupdf
import re
import pandas as pd
import os
import logging
from dotenv import load_dotenv

load_dotenv()
INPUT_DATA_PATH = os.getenv("INPUT_DATA_PATH")
OUTPUT_DATA_PATH = os.getenv("OUTPUT_DATA_PATH")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extrair_dados_allianz_auto(texto):
    dados = {
        "MÊS": [""],
        "SEGURADORA": ["Allianz"],
        "SEGURADO": [""],
        "CPF/CNPJ": [""],
        "CEP": [""],
        "PROPOSTA": [""],
        "APÓLICE": [""],
        "ENDOSSO": [""],
        "RAMO": ["Auto"],
        "VEÍCULO": [""],
        "PLACA": [""],
        "PRÊMIO LÍQUIDO": [""],
        "PRÊMIO TOTAL": [""],
        "VIGÊNCIA": [""],
        "QUANTIDADE DE PARCELAS": [""],
        "PARCELA 1": [""],
        "PARCELA 2": [""],
        "PARCELA 3": [""],
        "PARCELA 4": [""],
        "PARCELA 5": [""],
        "PARCELA 6": [""],
        "PARCELA 7": [""],
        "PARCELA 8": [""],
        "PARCELA 9": [""],
        "PARCELA 10": [""],
        "PARCELA 11": [""],
        "PARCELA 12": [""],
        "FORMA DE PAGAMENTO": [""],
        "COMISSÃO APLICADA": [""],
    }

    segurado1 = re.search(r"Segurado:\s*(.*?)\s*CPF/CNPJ", texto)
    segurado2 = re.search(r"Segurado:\s*(.*?)\s*Nome", texto)

    if segurado1:
        dados["SEGURADO"][0] = segurado1.group(1).strip()
    elif segurado2 and not (segurado2 == "None"):
        dados["SEGURADO"][0] = segurado2.group(1).strip()

    cpf = re.search(r"CPF/CNPJ:\s*([\d\.\-V]+)", texto)
    if cpf:
        dados["CPF/CNPJ"][0] = cpf.group(1)

    cep = re.search(r"CEP Pernoite:\s*(\d{5}-\d{3})", texto)
    if cep:
        dados["CEP"][0] = cep.group(1)

    proposta = re.search(r"Proposta Nº.:\s*(\d+)", texto)
    if proposta:
        dados["PROPOSTA"][0] = proposta.group(1)

    apolice = re.search(r"Apólice Nº.:\s*(\w+)", texto)
    if apolice:
        dados["APÓLICE"][0] = apolice.group(1)

    endosso = re.search(r"Endosso Nº.:\s*(\w+)", texto)
    if endosso:
        dados["ENDOSSO"][0] = endosso.group(1)
    else:
        dados["ENDOSSO"][0] = 0

    placa = re.search(r"Placa:\s*(\w+\d+)", texto)
    if placa:
        dados["PLACA"] = placa.group(1)

    premio_liquido = re.search(r"Preço Líquido\s*R\$\s*([\d,\.]+)", texto)
    if premio_liquido:
        dados["PRÊMIO LÍQUIDO"][0] = "R$ " + premio_liquido.group(1).replace(
            " ", ""
        ).replace(".", ",")

    premio_total = re.search(
        r"Preço Total\s*\(impostos inclusos\)\s*R\$\s([\d,\.]+)", texto
    )
    if premio_total:
        dados["PRÊMIO TOTAL"][0] = "R$ " + premio_total.group(1).replace(
            " ", ""
        ).replace(".", ",")

    vigencia = re.search(
        r"Vigência:\s*das 24H de (\d{2}/\d{2}/\d{4}) às 24H de (\d{2}/\d{2}/\d{4})",
        texto,
    )
    if vigencia:
        dados["VIGÊNCIA"][0] = f"{vigencia.group(1)} a {vigencia.group(2)}"

    parcelas = re.findall(r"(\d{2}/\d{2}/\d{4})\s*R\$\s*[\d,\.]+", texto)
    dados["QUANTIDADE DE PARCELAS"][0] = len(parcelas)
    for i, data in enumerate(parcelas):
        if i < 12:
            dados[f"PARCELA {i+1}"][0] = data

    forma_pagamento = re.search(
        r"Forma de pagamento\s*(.*?)\s*(?:Débito|Crédito em \d+ parcelas|$)",
        texto,
        re.DOTALL,
    )
    if forma_pagamento:
        dados["FORMA DE PAGAMENTO"][0] = forma_pagamento.group(1).strip()

    veiculo = re.search(r"Veículo:\s*([\w.]+)", texto)
    if veiculo:
        dados["VEÍCULO"][0] = veiculo.group(1).strip()

    return dados


def processar_pdf(pdf_path):
    try:
        documento = pymupdf.open(pdf_path)
        texto = ""
        for pagina in documento:
            texto += pagina.get_text()
        dados_extraidos = extrair_dados_allianz_auto(texto)
        return dados_extraidos
    except Exception as e:
        logging.exception(f"Erro ao processar o arquivo Pdf: {e}")
        return f"Erro ao processar o arquivo PDF: {e}"


def gerar_planilha(dados, output_path):
    df = pd.DataFrame(dados)
    df.to_excel(output_path, index=False)
    logging.info(f"Planilha gerada com sucesso em {output_path}")


def processar_multiplos_pdfs(pdf_paths):
    dados_acumulados = []
    for pdf_path in pdf_paths:
        dados = processar_pdf(pdf_path)
        if isinstance(dados, dict):
            dados_acumulados.append(pd.DataFrame(dados))
        else:
            logging.warning(f"Falha ao processar o PDF: {pdf_path}. Detalhes: {dados}")
    if dados_acumulados:
        df_final = pd.concat(dados_acumulados, ignore_index=True)
        output_path = OUTPUT_DATA_PATH
        gerar_planilha(df_final, output_path)
        return output_path
    else:
        logging.warning("Nenhum dado foi extraído.")
        return "Nenhum dados foi extraídos."


pdf_paths = []
for i in os.listdir(INPUT_DATA_PATH):
    path_folder = "input_pdfs/"
    path = f"{path_folder}{i}"
    pdf_paths.append(path)

output_file = processar_multiplos_pdfs(pdf_paths)
output_file
