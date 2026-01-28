# Classificador de Dados Pessoais - Hackathon Participa DF

## 1. Objetivo da Solução

Este projeto foi desenvolvido para o desafio de **Acesso à Informação** do Hackathon Participa DF. Sua principal função é analisar um conjunto de pedidos de acesso à informação e **identificar automaticamente aqueles que contêm dados pessoais**, classificando-os como "RESTRITO".

A solução utiliza uma abordagem híbrida:

1.  **Expressões Regulares (Regex):** Para detectar padrões de dados estruturados como CPF, e-mail e telefone.
2.  **Inteligência Artificial (NLP):** Com o uso da biblioteca `spacy` e do modelo `pt_core_news_lg`, para identificar entidades nominais como nomes de pessoas, que não seguem um padrão fixo.

O objetivo é maximizar a precisão e a sensibilidade (recall) do modelo, garantindo que o menor número possível de dados pessoais passe sem ser detectado (falsos negativos).

---

## 2. Estrutura de Arquivos do Projeto

A estrutura de pastas foi organizada para separar claramente os dados dos scripts, conforme a lógica do projeto:

| Pasta / Arquivo           | Descrição                                                                                              |
| :------------------------ | :----------------------------------------------------------------------------------------------------- |
| **`📂 dados/entrada/`**   | Local onde o arquivo de amostra (`AMOSTRA_e-SIC.xlsx`) deve ser colocado.                              |
| **`📂 dados/saida/`**     | Local onde o script salva o resultado da análise (`resultado_analise.csv`).                            |
| **`📂 src/`**             | Contém os módulos Python com a lógica de análise.                                                      |
| **`📄 src/analise.py`**   | Contém as funções de detecção de dados pessoais (Regex e IA).                                          |
| **`📄 main.py`**          | O "cérebro" do projeto. Orquestra a leitura, o processamento e a gravação dos resultados.              |
| **`📄 requirements.txt`** | Arquivo de configuração que lista todas as bibliotecas Python necessárias para que o projeto funcione. |

---

## 3. Pré-requisitos

Antes de iniciar, garanta que você tenha os seguintes softwares instalados em sua máquina:

- **Python 3.9 ou superior.**

---

## 4. Instruções de Instalação e Configuração

Siga **exatamente** esta sequência de comandos no seu terminal para preparar o ambiente de execução.

**a) Crie o Ambiente Virtual**
Este comando cria uma pasta `.venv` que conterá todas as dependências do projeto.

```bash
python3 -m venv .venv
```

**b) Ative o Ambiente Virtual**
Este comando "liga" o ambiente. Você deve executá-lo sempre que abrir um novo terminal para trabalhar no projeto.

```bash
# No Linux ou macOS
source .venv/bin/activate
```

**c) Instale as Dependências**
Este comando lê o arquivo `requirements.txt` e instala automaticamente todas as bibliotecas necessárias.

```bash
pip install -r requirements.txt
```

**d) Baixe o Modelo de IA**
Este comando faz o download do modelo de linguagem em português que o `spacy` utilizará.

```bash
python -m spacy download pt_core_news_lg
```

---

## 5. Instruções de Execução

**a) Comando de Execução**
Com o ambiente virtual ativo e o arquivo `AMOSTRA_e-SIC.xlsx` dentro da pasta `dados/entrada/`, execute o seguinte comando no terminal:

```bash
python main.py
```

**b) Formato dos Dados de Entrada e Saída**

- **Entrada:** O script espera encontrar um arquivo Excel (`.xlsx`) no caminho `dados/entrada/AMOSTRA_e-SIC.xlsx`. Este arquivo deve conter as colunas `ID` e `Texto Mascarado`.

- **Saída:** Após a execução, o script criará um arquivo CSV em `dados/saida/resultado_analise.csv` com as colunas `ID`, `Classificacao` e `Justificativa`.
