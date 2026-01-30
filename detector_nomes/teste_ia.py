import spacy

# Carrega o modelo de IA. 
# Dica: Se o seu PC for rápido, use "pt_core_news_lg" para mais precisão.
nlp = spacy.load("pt_core_news_sm")

# Filtros específicos para o contexto do DF
SIGLAS_DF = ["SQS", "SQN", "SHIS", "SHIN", "QNM", "QNJ", "QNL", "GDF", "DETRAN", "DER", "RA"]
INSTITUICOES = ["SECRETARIA", "MINISTÉRIO", "OUVIDORIA", "CONTROLADORIA", "POLÍCIA", "HOSPITAL", "COORDENAÇÃO"]

def tem_nome_pessoa(texto: str) -> bool:
    """
    Missão da Pessoa 3: Detectar nomes de cidadãos (Dados Pessoais)
    """
    if not texto or not isinstance(texto, str):
        return False

    # Processamos o texto com a IA
    doc = nlp(texto)

    for ent in doc.ents:
        # PER é a etiqueta da IA para 'Pessoa'
        if ent.label_ == "PER":
            nome_achado = ent.text.upper().strip()
            
            # FILTRO 1: Ignorar se for um órgão ou sigla do DF
            if any(sigla in nome_achado for sigla in SIGLAS_DF):
                continue
            
            # FILTRO 2: Ignorar se for uma instituição
            if any(inst in nome_achado for inst in INSTITUICOES):
                continue

            # FILTRO 3: Validar se não é um endereço (checa palavra anterior)
            start_token = ent.start
            if start_token > 0:
                token_anterior = doc[start_token - 1].text.lower()
                if token_anterior in ["rua", "lote", "quadra", "bloco", "conjunto"]:
                    continue

            # Se passar pelos filtros, é um nome que precisa ser protegido!
            return True

    return False