# 📊 Análise de Dados Inteligente - Hackathon

Este projeto realiza o processamento de linguagem natural (NLP) em dados públicos (e-SIC/Participa DF) utilizando Python, Pandas e Spacy. O objetivo é classificar e analisar demandas automaticamente.

---

## 📂 Estrutura de Pastas

Aqui está a organização do projeto e para que serve cada coisa:

| Pasta / Arquivo           | Descrição                                                                                                                                                                               |
| :------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`📂 dados/`**           | **Entrada e Saída.** Coloque seus arquivos CSV/Excel originais aqui. O script também salvará os resultados processados nesta pasta.                                                     |
| **`📂 .venv/`**           | **Ambiente Virtual.** É uma pasta gerada automaticamente que contém todas as bibliotecas instaladas (Pandas, Spacy) isoladas do seu sistema operacional. **Não mexa aqui manualmente.** |
| **`📄 main.py`**          | **O Código Principal.** É o "cérebro" da automação. Ele lê o arquivo da pasta `dados/`, processa com IA e gera o relatório.                                                             |
| **`📄 requirements.txt`** | **Lista de Dependências.** Um arquivo de texto que diz ao instalador (`pip`) quais bibliotecas e versões o projeto precisa para funcionar.                                              |

---

## 🚀 Como Rodar o Projeto

Siga estes passos se estiver baixando o projeto pela primeira vez ou reiniciou o computador.

### 1. Preparar o Ambiente (Apenas na 1ª vez)

Crie o ambiente virtual para isolar as dependências:

```bash
python3 -m venv .venv

2. Ativar o Ambiente (Sempre que abrir o terminal)

Antes de rodar qualquer comando, certifique-se de que o ambiente está ativo (o texto (.venv) aparecerá no terminal).

No Linux/Mac:
Bash

source .venv/bin/activate

3. Instalar Dependências

Instale o Pandas, Spacy e baixe o modelo de inteligência artificial em português (obrigatório):
Bash

pip install -r requirements.txt
python -m spacy download pt_core_news_lg

4. Executar

Certifique-se de que o arquivo de dados (ex: AMOSTRA_e-SIC.csv) está dentro da pasta dados/ e rode:
Bash

python main.py

🛠 Solução de Problemas Comuns

Erro: "ModuleNotFoundError: No module named 'pandas'"

    Causa: Você esqueceu de ativar o ambiente virtual.

    Solução: Rode source .venv/bin/activate.

Erro: "Can't find model 'pt_core_news_lg'"

    Causa: As bibliotecas estão instaladas, mas o "cérebro" da IA não foi baixado.

    Solução: Rode python -m spacy download pt_core_news_lg.

Erro: "No such file or directory"

    Causa: O código não achou o arquivo CSV.

    Solução: Verifique se o nome do arquivo no código bate exatamente com o nome do arquivo na pasta dados/.


---

### Próximo passo sugerido
Agora que você tem o `README.md` e o `requirements.txt`, seu projeto está **muito mais profissional**. Se você subir isso para o GitHub, os juízes do Hackathon vão conseguir rodar seu código sem dor de cabeça.

Quer ajuda para ajustar o código do `main.py` para ele ler automaticamente da pasta `dad
```
