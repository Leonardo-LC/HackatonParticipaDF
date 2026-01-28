import re

# --- FUNÇÕES DE ANÁLISE E DETECÇÃO ---

def normalizar_texto(texto):
    """
    Realiza uma limpeza básica no texto, removendo quebras de linha
    e espaços múltiplos.
    """
    if not isinstance(texto, str):
        return ""

    texto = texto.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    texto = " ".join(texto.split())
    return texto


def tem_padrao_fixo(texto):
    """
    Busca por padrões fixos (Regex) de CPF, Email e Telefone no texto.
    Retorna True e o motivo se encontrar algo.
    """
    if not isinstance(texto, str):
        return False, None
        
    regex_cpf = r'(?:\d{3}\.?\d{3}\.?\d{3}-?\d{2})'
    regex_email = r'[\w\.-]+@[\w\.-]+\.\w+'
    regex_tel = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'

    if re.search(regex_cpf, texto):
        return True, "CPF Detectado"
    if re.search(regex_email, texto):
        return True, "Email Detectado"
    if re.search(regex_tel, texto):
        return True, "Telefone Detectado"
        
    return False, None

def tem_nome_pessoa(texto, nlp_model):
    """
    Utiliza o modelo do Spacy para encontrar nomes de pessoas (entidade PER).
    Retorna True se encontrar um nome com mais de uma palavra.
    """
    if not isinstance(texto, str):
        return False
        
    doc = nlp_model(texto)
    for entidade in doc.ents:
        if entidade.label_ == "PER":
            if len(entidade.text.split()) > 1: 
                return True
    return False
