import re
from PyPDF2 import PdfReader
from datetime import datetime

def extrair_campos_pdf(path_pdf):
    reader = PdfReader(path_pdf)
    texto = ""
    for pagina in reader.pages:
        pagina_texto = pagina.extract_text()
        if pagina_texto:
            texto += pagina_texto + "\n"

    dados = {}

    # Nome / Razão Social (mantendo o regex antigo, que funcionava)
    match_nome = re.search(
        r"NOME/RAZÃO SOCIAL\s*([\w\s\.]+)\s+\d{3}\.\d{3}\.\d{3}-\d{2}", texto
    )
    if match_nome:
        dados["nome"] = match_nome.group(1).strip()

    # Captura apenas o bloco do destinatário
    match_destinatario = re.search(
        r"DESTINATÁRIO / REMETENTE\s*\n([\s\S]+?)\n(?:DATA|$)", texto
    )
    if match_destinatario:
        bloco = match_destinatario.group(1).strip()

        # CEP
        match_cep = re.search(r"(\d{5}-?\d{3})", bloco)
        if match_cep:
            dados["cep"] = match_cep.group(1)

        # Bairro: procura "Bairro: NomeBairro" ou depois de hífen
        match_bairro = re.search(r"Bairro[:\s]*([A-Za-zÀ-ÿ\s]+)", bloco)
        if match_bairro:
            dados["bairro"] = match_bairro.group(1).strip()
        else:
            # tenta pegar após hífen
            match_bairro2 = re.search(r"-(.+?),", bloco)
            dados["bairro"] = match_bairro2.group(1).strip() if match_bairro2 else "Não informado"

        # Endereço: primeira linha do bloco sem CEP e bairro
        endereco = re.sub(r"\d{5}-?\d{3}", "", bloco)
        endereco = re.sub(r"Bairro[:\s]*[A-Za-zÀ-ÿ\s]+", "", endereco)
        dados["endereco"] = endereco.split("\n")[0].strip()

        # Cidade e UF: procura padrão "Cidade / UF"
        match_cidade_uf = re.search(r"([A-Za-zÀ-ÿ\s]+)[\s\/]+([A-Z]{2})", bloco)
        if match_cidade_uf:
            dados["cidade"] = match_cidade_uf.group(1).strip()
            dados["uf"] = match_cidade_uf.group(2).strip()
        else:
            dados["cidade"] = "Não identificada"
            dados["uf"] = "NA"

    # Data de emissão (continua procurando no texto inteiro)
    match_data = re.search(r"DATA DA EMISSÃO\s*\n(\d{2}/\d{2}/\d{4})", texto)
    if match_data:
        try:
            dados["data_emissao"] = datetime.strptime(match_data.group(1), "%d/%m/%Y").date()
        except ValueError:
            dados["data_emissao"] = None
    else:
        match_data2 = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", texto)
        if match_data2:
            dados["data_emissao"] = datetime.strptime(match_data2.group(1), "%d/%m/%Y").date()
        else:
            dados["data_emissao"] = None

    return dados
