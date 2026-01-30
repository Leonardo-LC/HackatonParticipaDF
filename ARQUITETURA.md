# Documentação Técnica

## Visão Geral

O sistema classifica documentos de acesso à informação em PUBLICO ou RESTRITO detectando dados pessoais através de dois mecanismos complementares: análise por padrões estruturados (Regex) e processamento de linguagem natural (NLP).

## Pipeline de Processamento

```
Arquivo Excel
    ↓
Normalização de Texto
    ↓
┌─────────────────────────────┐
│  Análise Padrão Fixo (Regex)│
│  - CPF                      │
│  - Email                    │
│  - Telefone                 │
└──────────┬──────────────────┘
           ↓
    Encontrou? SIM → RESTRITO
           │
           NO
           ↓
┌─────────────────────────────┐
│  Análise IA (Spacy NER)     │
│  - NER (Named Entities)     │
│  - Filtros Inteligentes     │
│  - Fallback Contextual      │
└──────────┬──────────────────┘
           ↓
    Encontrou? SIM → RESTRITO
           │
           NO
           ↓
        PUBLICO
```

## Módulos

### main.py

**Responsabilidade**: Orquestração do pipeline

Assinatura:

```python
processar_arquivo(caminho_entrada=None, caminho_saida=None)
```

Parâmetros:

- `caminho_entrada` - Caminho do arquivo Excel (padrão: `dados/entrada/AMOSTRA_e-SIC.xlsx`)
- `caminho_saida` - Caminho do arquivo CSV (padrão: `dados/saida/resultado_analise.csv`)

Uso via CLI:

```bash
python main.py                                    # Usa padrões
python main.py entrada.xlsx                      # Entrada customizada
python main.py entrada.xlsx saida.csv            # Entrada e saída customizadas
```

Fluxo:

1. Carrega modelo Spacy `pt_core_news_lg`
2. Lê arquivo Excel
3. Itera sobre cada linha
4. Aplica funções de detecção de `src/analise.py`
5. Classifica cada documento
6. Salva resultado em `dados/saida/resultado_analise.csv`

### src/analise.py

**Responsabilidade**: Motor de detecção

#### Funções Auxiliares

- `normalizar_texto(texto)` - Remove quebras de linha e espaços extras
- `_limpa(txt)` - Limpeza agressiva de espaços
- `_tem_palavra_lista(texto, lista)` - Busca de palavras com word boundary

#### Detecção por Regex

`tem_padrao_fixo(texto)` → (bool, motivo)

Padrões:

- CPF: `\d{3}\.?\d{3}\.?\d{3}-?\d{2}`
- Email: `[\w\.-]+@[\w\.-]+\.\w+`
- Telefone: `\(?\d{2}\)?\s?\d{4,5}-?\d{4}`

Retorna:

- `(True, "CPF Detectado")` ou `(True, "Email Detectado")` ou `(True, "Telefone Detectado")`
- `(False, None)` se nenhum padrão encontrado

#### Detecção por IA

`extrair_nomes(texto, nlp_model)` → List[Dict]

Retorna lista com nomes encontrados:

```python
[
  {
    "tipo": "NOME",
    "valor": "João Silva",
    "pos": [inicio, fim],
    "metodo": "NER" ou "CONTEXTO_REGEX",
    "confianca": 0.75
  }
]
```

Processo:

1. **NER (Named Entity Recognition)**
   - Busca entidades com `label_ == "PER"`
   - Aplica 4 filtros:
     - Remove caracteres especiais/números
     - Remove órgãos institucionais
     - Valida tamanho (2-6 tokens)
     - Remove contexto local (endereços)

2. **Fallback Contextual**
   - Padrão Regex: `\b(me chamo|meu nome é|meu nome e|eu)\s*,?\s*([A-Za-zÀ-ÿ]{2,})\b`
   - Detecta expressões diretas

`tem_nome_pessoa(texto, nlp_model)` → bool

Wrapper que retorna `True` se houver qualquer nome detectado.

#### Listas de Filtros

**FILTRO_INSTITUCIONAL** (35+ termos):

- SECRETARIA, GOVERNO, MINISTÉRIO, PREFEITURA
- ÓRGÃO, AUTARQUIA, EMPRESA, BANCO
- PROTOCOLO, PROCESSO, DOCUMENTO, etc.

**CONTEXTO_LOCAL** (15+ palavras):

- RUA, QUADRA, LOTE, BLOCO, AVENIDA
- CONDOMÍNIO, SETOR, CEP, etc.

### teste_completo.py

**Responsabilidade**: Validação do sistema

Testa:

1. **7 casos manuais** - Diferentes tipos de entrada
2. **10 linhas do arquivo real** - Processamento real
3. **Estatísticas** - Contagem de RESTRITO/PUBLICO

## Configuração

### Formato de Entrada

Arquivo Excel com colunas obrigatórias:

- **ID** - Identificador único do documento
- **Texto Mascarado** - Conteúdo a ser analisado

### Formato de Saída

Arquivo CSV com separador `;` (ponto e vírgula):

- **ID** - Identificador único
- **Classificacao** - PUBLICO ou RESTRITO
- **Justificativa** - Motivo da classificação

Exemplo:

```
ID;Classificacao;Justificativa
1;PUBLICO;Nenhum dado sensível encontrado
7;RESTRITO;CPF Detectado
8;RESTRITO;Possível Nome Pessoal (IA)
```

## Performance

- Carregamento modelo: ~3 segundos
- Processamento: ~20 documentos/segundo
- 99 linhas: ~5 segundos total

## Dependências

```
pandas==3.0.0
spacy==3.8.11
openpyxl==3.1.5
pt-core-news-lg==3.8.0
```

## Estrutura de Diretórios

```
src/
├── analise.py                  # Motor de detecção
dados/
├── entrada/
│   └── AMOSTRA_e-SIC.xlsx      # Entrada
└── saida/
## Estrutura de Diretórios

```

src/
├── analise.py # Motor de detecção

main.py # Orquestração
test.py # Validação

```

## Fluxo de Dados

```

Arquivo Excel
↓
main.py (lê arquivo)
↓
Para cada linha:
├─ ID, Texto Mascarado
├─ normalizar_texto()
├─ tem_padrao_fixo()
│ └─ Encontrou? → RESTRITO
└─ tem_nome_pessoa()
└─ Encontrou? → RESTRITO
└─ Senão → PUBLICO
↓
DataFrame com resultados
↓
Arquivo CSV

```

## Tratamento de Erros

Validações implementadas:
- Arquivo não encontrado → Mensagem de erro
- Coluna não encontrada → Mensagem de erro, exit
- Modelo Spacy não instalado → Mensagem de erro, exit
- Diretório de saída não existe → Criado automaticamente

## Extensibilidade

Para adicionar novo padrão Regex:
1. Editar `tem_padrao_fixo()` em `src/analise.py`
2. Adicionar novo `re.search()`

Para ajustar sensibilidade NER:
1. Editar `FILTRO_INSTITUCIONAL` ou `CONTEXTO_LOCAL`
2. Ajustar tamanho de tokens em `extrair_nomes()`

Para usar modelo Spacy diferente:
1. Alterar `spacy.load()` em `main.py`
2. Baixar novo modelo: `python -m spacy download MODELO_NOVO`

1. Alterar `spacy.load()` em `main.py`
2. Baixar novo modelo: `python -m spacy download pt_core_news_sm`
```
