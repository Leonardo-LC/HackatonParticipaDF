import pandas as pd
import spacy
import re
import sys
import os

# --- CONFIGURAÇÃO INICIAL ---
print("Carregando modelo de IA (pode demorar um pouco)...")
try:
    nlp = spacy.load("pt_core_news_lg")
except:
    print("ERRO: Modelo do Spacy não encontrado.")
    print("Rode no terminal: python -m spacy download pt_core_news_lg")
    sys.exit()

# --- FUNÇÕES DE DETECÇÃO ---

def tem_padrao_fixo(texto):
    if not isinstance(texto, str):
        return False, ""
        
    regex_cpf = r'(?:\d{3}\.?\d{3}\.?\d{3}-?\d{2})'
    regex_email = r'[\w\.-]+@[\w\.-]+\.\w+'
    
    regex_tel = r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}'

    if re.search(regex_cpf, texto):
        return True, "CPF Detectado"
    if re.search(regex_email, texto):
        return True, "Email Detectado"
    if re.search(regex_tel, texto):
        return True, "Telefone Detectado"
        
    return False, ""

def tem_nome_pessoa(texto):
    if not isinstance(texto, str):
        return False
        
    doc = nlp(texto)
    for entidade in doc.ents:
        if entidade.label_ == "PER":
            if len(entidade.text.split()) > 1: 
                return True
    return False

# --- BLOCO PRINCIPAL ---

def processar_arquivo():
    # 1. NOME CORRIGIDO PARA .XLSX
    caminho_entrada = os.path.join("dados", "entrada", "AMOSTRA_e-SIC.xlsx")
    caminho_saida = os.path.join("dados", "saida", "resultado_analise.csv")
    
    if not os.path.exists(caminho_entrada):
        print(f"❌ ERRO CRÍTICO: Arquivo não encontrado!")
        print(f"O script procurou em: {caminho_entrada}")
        return

    print(f"📂 Lendo arquivo de: {caminho_entrada}")
    
    # 2. COMANDO CORRIGIDO PARA LER EXCEL
    try:
        df = pd.read_excel(caminho_entrada) 
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return

    resultados = []
    total = len(df)
    print(f"Iniciando análise de {total} linhas...")
    
    for index, linha in df.iterrows():
        if index % 100 == 0:
            print(f"Processando linha {index}/{total}...")

        try:
            id_pedido = linha['ID']
            texto = linha['Texto Mascarado']
        except KeyError as e:
            print(f"❌ Erro: Coluna não encontrada: {e}")
            print(f"Colunas disponíveis: {list(df.columns)}")
            return
        
        encontrou_padrao, motivo = tem_padrao_fixo(texto)
        
        classificacao = "PUBLICO"
        justificativa = "Nenhum dado sensível encontrado"

        if encontrou_padrao:
            classificacao = "RESTRITO"
            justificativa = motivo
        elif tem_nome_pessoa(texto):
            classificacao = "RESTRITO"
            justificativa = "Possível Nome Pessoal (IA)"

        resultados.append({
            'ID': id_pedido,
            'Classificacao': classificacao,
            'Justificativa': justificativa,
            'Texto Analisado': texto
        })

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df_saida = pd.DataFrame(resultados)
    df_saida.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"✅ Concluído com sucesso!")
    print(f"Arquivo salvo em: {caminho_saida}")

if __name__ == "__main__":
    processar_arquivo()