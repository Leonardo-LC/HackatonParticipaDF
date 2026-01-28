import pandas as pd
import spacy
import sys
import os

# Importa as funções de análise do novo arquivo
from src.analise import normalizar_texto, tem_padrao_fixo, tem_nome_pessoa

# --- BLOCO PRINCIPAL ---

def processar_arquivo():
    """
    Função principal que orquestra a leitura, análise e gravação dos dados.
    """
    # --- CONFIGURAÇÃO INICIAL ---
    print("Carregando modelo de IA (pode demorar um pouco)...")
    try:
        nlp = spacy.load("pt_core_news_lg")
    except OSError:
        print("ERRO: Modelo do Spacy não encontrado.")
        print("Execute no terminal: python -m spacy download pt_core_news_lg")
        sys.exit()

    # Define os caminhos de entrada e saída
    caminho_entrada = os.path.join("dados", "entrada", "AMOSTRA_e-SIC.xlsx")
    caminho_saida = os.path.join("dados", "saida", "resultado_analise.csv")
    
    if not os.path.exists(caminho_entrada):
        print(f"❌ ERRO CRÍTICO: Arquivo não encontrado!")
        print(f"O script procurou em: {caminho_entrada}")
        return

    print(f"📂 Lendo arquivo de: {caminho_entrada}")
    
    try:
        df = pd.read_excel(caminho_entrada) 
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")
        return

    resultados = []
    total = len(df)
    print(f"Iniciando análise de {total} linhas...")
    
    # Itera sobre cada linha do DataFrame
    for index, linha in df.iterrows():
        if index > 0 and index % 100 == 0:
            print(f"Processando linha {index}/{total}...")

        try:
            id_pedido = linha['ID']
            texto_original = linha['Texto Mascarado']
            
            # Usa a função de normalização importada
            texto = normalizar_texto(texto_original)

        except KeyError as e:
            print(f"❌ Erro: Coluna não encontrada no arquivo Excel: {e}")
            print(f"Verifique se as colunas 'ID' e 'Texto Mascarado' existem.")
            return
        
        # Usa as funções de detecção importadas
        encontrou_padrao, motivo = tem_padrao_fixo(texto)
        
        classificacao = "PUBLICO"
        justificativa = "Nenhum dado sensível encontrado"

        if encontrou_padrao:
            classificacao = "RESTRITO"
            justificativa = motivo
        # Passa o modelo 'nlp' como argumento para a função
        elif tem_nome_pessoa(texto, nlp):
            classificacao = "RESTRITO"
            justificativa = "Possível Nome Pessoal (IA)"

        resultados.append({
            'ID': id_pedido,
            'Classificacao': classificacao,
            'Justificativa': justificativa,
        })

    # Garante que o diretório de saída exista
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    df_saida = pd.DataFrame(resultados)
    df_saida.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"✅ Concluído com sucesso!")
    print(f"Arquivo salvo em: {caminho_saida}")

# --- PONTO DE ENTRADA DO SCRIPT ---
if __name__ == "__main__":
    processar_arquivo()
