import re
from PyPDF2 import PdfReader
from datetime import datetime

def extrair_campos_pdf(path_pdf):
    reader = PdfReader(path_pdf)
    texto = ""
    for pagina in reader.pages:
        texto += pagina.extract_text() + "\n"

    dados = {}

    # Nome / Razão Social
    match_nome = re.search(r"NOME/RAZÃO SOCIAL\s*([\w\s\.]+)\s+\d{3}\.\d{3}\.\d{3}-\d{2}", texto)
    if match_nome:
        dados["nome"] = match_nome.group(1).strip()

    # Endereço (linha após DESTINATÁRIO / REMETENTE)
    match_endereco = re.search(r"DESTINATÁRIO / REMETENTE\s*\n(.+)", texto)
    if match_endereco:
        endereco_linha = match_endereco.group(1).strip()
        # Exemplo: "Rua Engenheiro Alcindo Trindade, 124 - Casa Constestado 95690000"
        dados["endereco"] = re.sub(r"\d{5}-?\d{3}", "", endereco_linha).strip()

        # CEP
        match_cep = re.search(r"(\d{5}-?\d{3})", endereco_linha)
        if match_cep:
            dados["cep"] = match_cep.group(1)

    # Cidade e UF (na linha seguinte)
    match_cidade_uf = re.search(r"\n([A-Za-z\s]+)\s([A-Z]{2})\n", texto)
    if match_cidade_uf:
        dados["cidade"] = match_cidade_uf.group(1).strip()
        dados["uf"] = match_cidade_uf.group(2).strip()

    # Bairro (opcional, pode estar em outra parte do texto)
    match_bairro = re.search(r"Bairro:\s*([A-Za-z\s]+)[,\.]", texto)
    if match_bairro:
        dados["bairro"] = match_bairro.group(1).strip()
    else:
        dados["bairro"] = "Não informado"

    # Data de emissão
    match_data = re.search(r"DATA DA EMISSÃO\s*\n(\d{2}/\d{2}/\d{4})", texto)
    if match_data:
        try:
            dados["data_emissao"] = datetime.strptime(match_data.group(1), "%d/%m/%Y").date()
        except ValueError:
            dados["data_emissao"] = None
    else:
        # fallback: primeira data no documento
        match_data2 = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", texto)
        if match_data2:
            dados["data_emissao"] = datetime.strptime(match_data2.group(1), "%d/%m/%Y").date()

    return dados
