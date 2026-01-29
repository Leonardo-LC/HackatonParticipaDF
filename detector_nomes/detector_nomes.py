import re
import sys
import spacy
from typing import List, Dict, Any

# =========================
# CARREGAMENTO DO MODELO
# =========================
try:
    nlp = spacy.load("pt_core_news_sm")
except Exception:
    print("Erro: instale o modelo com 'python -m spacy download pt_core_news_sm'")
    sys.exit(1)

# =========================
# LISTAS DE FILTRO
# =========================
FILTRO_INSTITUCIONAL = [
    "SECRETARIA", "SECRETÁRIO", "GDF", "GOVERNO", "MINISTÉRIO", "ADMINISTRAÇÃO",
    "OUVIDORIA", "DEPARTAMENTO", "DIRETORIA", "COMPANHIA", "EMPRESA", "AUTARQUIA",
    "VALIDADOR", "PROTOCOLO", "PROCESSO", "NOTA", "FISCAL", "EMPENHO", "EMENDA",
    "PARLAMENTAR", "PEDIDO", "RAZÃO", "SOCIAL", "CNPJ", "CPF", "E-MAIL", "EMAIL",
    "WHATSAPP", "ÓRGÃO", "ORGAO", "INSTITUTO", "POLÍCIA", "POLICIA", "MINISTÉRIO PÚBLICO",
    "PREFEITURA", "GABINETE", "COORDENAÇÃO", "COORDENACAO", "SETOR", "UNIDADE", "SISTEMA",
    "VALOR", "DOCUMENTO", "CONVÊNIO", "CONVENIO", "EMENDA"
]

CONTEXTO_LOCAL = [
    "RUA", "LOTE", "QUADRA", "BLOCO", "CONJUNTO", "TRECHO", "AVENIDA",
    "SETOR", "CONDOMÍNIO", "CONDOMINIO", "CEP", "ALAMEDA", "TRAVESSA",
    "RODOVIA", "KM", "Nº", "NUMERO", "NÚMERO"
]

# Contextos fortes para “nome isolado” (1 token) ou assinatura curta
# Ex.: "Me chamo Braga", "Meu nome é Ana", "Eu, Carlos, ..."
PADRAO_NOME_CURTO = re.compile(
    r"\b(me chamo|meu nome é|meu nome e|eu)\s*,?\s*([A-Za-zÀ-ÿ]{2,})\b",
    flags=re.IGNORECASE
)

# =========================
# FUNÇÕES AUXILIARES
# =========================
def _limpa(txt: str) -> str:
    return re.sub(r"\s+", " ", txt.replace("\n", " ")).strip()

def _tem_palavra_lista(texto_upper: str, lista: List[str]) -> bool:
    # Busca por palavra inteira (\b) para reduzir falsos positivos
    return any(re.search(rf"\b{re.escape(t)}\b", texto_upper) for t in lista)

# =========================
# FUNÇÃO PRINCIPAL
# =========================
def extrair_nomes(texto: str) -> List[Dict[str, Any]]:
    if not texto or not isinstance(texto, str):
        return []

    doc = nlp(texto)

    achados: List[Dict[str, Any]] = []
    vistos = set()

    # ---------- 1) NER ----------
    for ent in doc.ents:
        if ent.label_ != "PER":
            continue

        nome = _limpa(ent.text)
        nome_upper = nome.upper()

        # Filtros contra rótulos/metadata
        if any(ch in nome for ch in [":", "*"]) or "Nº" in nome_upper or re.search(r"\d", nome):
            continue

        # Elimina termos institucionais dentro do "nome"
        if _tem_palavra_lista(nome_upper, FILTRO_INSTITUCIONAL):
            continue

        # Heurística de tamanho: evita 1 token solto e evita trechos enormes “pegos” pelo NER
        tokens = [t for t in nome.split() if t.lower() not in ("da", "de", "do", "das", "dos")]
        if len(tokens) < 2 or len(tokens) > 6:
            continue

        # Contexto local imediatamente antes do nome (ex.: "Condomínio X", "Rua X")
        janela_inicio = max(0, ent.start_char - 40)
        contexto = texto[janela_inicio:ent.start_char].upper()
        if _tem_palavra_lista(contexto, CONTEXTO_LOCAL):
            continue

        # Dedup
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

    # ---------- 2) FALLBACK “nome curto” (rodar sempre) ----------
    # Serve para casos tipo "Me chamo Braga" mesmo quando já existem outros nomes no texto.
    m = PADRAO_NOME_CURTO.search(texto)
    if m:
        nome_fb = _limpa(m.group(2))
        key_fb = nome_fb.upper()

        # Evita lixo institucional e duplicados
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

def tem_nome_pessoa(texto: str) -> bool:
    return len(extrair_nomes(texto)) > 0

# =========================
# TESTE MANUAL
# =========================
if __name__ == "__main__":
    testes = [
        "O senhor João da Silva solicitou o reparo.",
        "Moro na Quadra João de Barro, lote 10.",
        "Solicitação feita por maria oliveira em 2024.",
        "A Secretaria de Saúde do DF solicitou informações.",
        "Nome: Maria",
        "Me chamo Braga e preciso de ajuda."
    ]
    print("\n=== TESTE FINAL (detector_nomes.py) ===")
    for t in testes:
        print("\nTEXTO:", t)
        print("DETECÇÃO:", extrair_nomes(t))
