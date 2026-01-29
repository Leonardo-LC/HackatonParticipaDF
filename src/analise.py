import re
from typing import List, Dict, Any

# =========================
# FUNÇÕES AUXILIARES
# =========================

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


def _limpa(txt: str) -> str:
    """Remove espaços extras e quebras de linha."""
    return re.sub(r"\s+", " ", txt.replace("\n", " ")).strip()


def _tem_palavra_lista(texto_upper: str, lista: List[str]) -> bool:
    """Busca por palavras inteiras na lista (evita falsos positivos)."""
    return any(re.search(rf"\b{re.escape(t)}\b", texto_upper) for t in lista)


# =========================
# LISTAS DE FILTROS
# =========================

FILTRO_INSTITUCIONAL = [
    "SECRETARIA", "SECRETÁRIO", "GDF", "GOVERNO", "MINISTÉRIO", "ADMINISTRAÇÃO",
    "OUVIDORIA", "DEPARTAMENTO", "DIRETORIA", "COMPANHIA", "EMPRESA", "AUTARQUIA",
    "VALIDADOR", "PROTOCOLO", "PROCESSO", "NOTA", "FISCAL", "EMPENHO", "EMENDA",
    "PARLAMENTAR", "PEDIDO", "RAZÃO", "SOCIAL", "CNPJ", "CPF", "E-MAIL", "EMAIL",
    "WHATSAPP", "ÓRGÃO", "ORGAO", "INSTITUTO", "POLÍCIA", "POLICIA", "MINISTÉRIO PÚBLICO",
    "PREFEITURA", "GABINETE", "COORDENAÇÃO", "COORDENACAO", "SETOR", "UNIDADE", "SISTEMA",
    "VALOR", "DOCUMENTO", "CONVÊNIO", "CONVENIO", "EMENDA", "CONTA", "BANCO"
]

CONTEXTO_LOCAL = [
    "RUA", "LOTE", "QUADRA", "BLOCO", "CONJUNTO", "TRECHO", "AVENIDA",
    "SETOR", "CONDOMÍNIO", "CONDOMINIO", "CEP", "ALAMEDA", "TRAVESSA",
    "RODOVIA", "KM", "Nº", "NUMERO", "NÚMERO"
]

PADRAO_NOME_CURTO = re.compile(
    r"\b(me chamo|meu nome é|meu nome e|eu)\s*,?\s*([A-Za-zÀ-ÿ]{2,})\b",
    flags=re.IGNORECASE
)


# =========================
# DETECÇÃO POR REGEX
# =========================

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


# =========================
# DETECÇÃO POR IA (SPACY)
# =========================

def extrair_nomes(texto: str, nlp_model) -> List[Dict[str, Any]]:
    """
    Extrai nomes de pessoas usando Spacy com filtros inteligentes.
    Retorna lista com nomes encontrados e informações.
    """
    if not texto or not isinstance(texto, str):
        return []

    doc = nlp_model(texto)
    achados: List[Dict[str, Any]] = []
    vistos = set()

    # ------- 1) DETECÇÃO POR NER (Named Entity Recognition) -------
    for ent in doc.ents:
        if ent.label_ != "PER":
            continue

        nome = _limpa(ent.text)
        nome_upper = nome.upper()

        # Filtro 1: Remove lixo com caracteres especiais ou números
        if any(ch in nome for ch in [":", "*"]) or "Nº" in nome_upper or re.search(r"\d", nome):
            continue

        # Filtro 2: Remove termos institucionais
        if _tem_palavra_lista(nome_upper, FILTRO_INSTITUCIONAL):
            continue

        # Filtro 3: Valida tamanho (não muito curto nem muito longo)
        tokens = [t for t in nome.split() if t.lower() not in ("da", "de", "do", "das", "dos")]
        if len(tokens) < 2 or len(tokens) > 6:
            continue

        # Filtro 4: Ignora endereços (contexto local antes do nome)
        janela_inicio = max(0, ent.start_char - 40)
        contexto = texto[janela_inicio:ent.start_char].upper()
        if _tem_palavra_lista(contexto, CONTEXTO_LOCAL):
            continue

        # Evita duplicatas
        key = nome_upper
        if key in vistos:
            continue
        vistos.add(key)

        achados.append({
            "tipo": "NOME",
            "valor": nome,
            "pos": [ent.start_char, ent.end_char],
            "metodo": "NER",
            "confianca": 0.75
        })

    # ------- 2) FALLBACK: CONTEXTO EXPLÍCITO -------
    # Para casos como "Me chamo João" mesmo se não detectar por NER
    m = PADRAO_NOME_CURTO.search(texto)
    if m:
        nome_fb = _limpa(m.group(2))
        key_fb = nome_fb.upper()

        if key_fb not in vistos and not _tem_palavra_lista(key_fb, FILTRO_INSTITUCIONAL):
            vistos.add(key_fb)
            achados.append({
                "tipo": "NOME",
                "valor": nome_fb,
                "pos": [m.start(2), m.end(2)],
                "metodo": "CONTEXTO_REGEX",
                "confianca": 0.60
            })

    return achados


def tem_nome_pessoa(texto: str, nlp_model) -> bool:
    """
    Verifica se há nome de pessoa no texto.
    Retorna True se encontrar qualquer nome.
    """
    if not isinstance(texto, str):
        return False
    
    nomes = extrair_nomes(texto, nlp_model)
    return len(nomes) > 0
