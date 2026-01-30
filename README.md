# Classificador de Dados Pessoais

Sistema automático para identificação e classificação de dados pessoais em pedidos de acesso à informação.

## Objetivo

Analisar documentos em formato texto e classificar automaticamente aqueles que contêm dados pessoais (CPF, email, telefone, nomes de pessoas) como RESTRITO, protegendo a privacidade conforme legislação de acesso à informação.

## Arquitetura

```
Arquivo Excel
      ↓
  main.py
      ↓
src/analise.py
  - Padrões fixos (CPF, Email, Telefone)
  - NER com filtros inteligentes
      ↓
Arquivo CSV
```

## Instalação

```bash
# 1. Criar ambiente virtual
python3 -m venv .venv

# 2. Ativar ambiente
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate      # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Baixar modelo de IA
python -m spacy download pt_core_news_lg
```

## Uso

### Validação do Sistema

```bash
python test.py
```

Executa testes de validação com casos de entrada comuns.

### Processamento de Arquivo

```bash
# Com caminhos padrão (dados/entrada/ → dados/saida/)
python main.py

# Com caminho de entrada customizado
python main.py caminho/entrada.xlsx

# Com caminhos de entrada e saída customizados
python main.py caminho/entrada.xlsx caminho/saida.csv
```

O script:

- Lê arquivo Excel
- Classifica cada documento
- Salva resultado em CSV

## Formato de Entrada

Arquivo Excel com colunas obrigatórias:

- **ID**: Identificador único do documento
- **Texto Mascarado**: Conteúdo a ser analisado

## Formato de Saída

CSV com separador `;`:

```
ID;Classificacao;Justificativa
1;PUBLICO;Nenhum dado sensível encontrado
7;RESTRITO;CPF Detectado
8;RESTRITO;Possível Nome Pessoal (IA)
```

### Classificações

- **PUBLICO**: Nenhum dado sensível detectado
- **RESTRITO**: Contém dados pessoais

### Justificativas

- CPF Detectado
- Email Detectado
- Telefone Detectado
- Possível Nome Pessoal (IA)
- Nenhum dado sensível encontrado

## Detecção

### Padrões Estruturados (Regex)

- **CPF**: 123.456.789-10 ou 12345678910
- **Email**: usuario@dominio.com
- **Telefone**: (11) 98765-4321 ou 11 98765-4321

### Detecção por IA (Spacy)

Utiliza modelo `pt_core_news_lg`:

1. **Named Entity Recognition (NER)** - Identifica entidades nomeadas
2. **Filtros Inteligentes** - Remove órgãos, endereços e falsas positivos
3. **Fallback Contextual** - Detecta expressões explícitas

## Troubleshooting

| Erro                         | Solução                                                 |
| ---------------------------- | ------------------------------------------------------- |
| `ModuleNotFoundError: spacy` | `pip install -r requirements.txt`                       |
| `Modelo não encontrado`      | `python -m spacy download pt_core_news_lg`              |
| `Arquivo não encontrado`     | Verifique caminho e nome do arquivo de entrada          |
| `Coluna não encontrada`      | Verifique se Excel tem colunas `ID` e `Texto Mascarado` |

## Dependências

- **pandas** - Processamento de dados
- **spacy** - Processamento de linguagem natural
- **openpyxl** - Leitura de arquivos Excel

## Estrutura de Arquivos

```
.
├── main.py                  # Script principal
├── teste_completo.py        # Validação do sistema
├── requirements.txt         # Dependências
├── ARQUITETURA.md          # Documentação técnica
├── src/
│   └── analise.py          # Motor de detecção
├── dados/
│   ├── entrada/            # Arquivos de entrada
│   └── saida/              # Resultados (gerado)
└── detector_nomes/         # Referência
```
