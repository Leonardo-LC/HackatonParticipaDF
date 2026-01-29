import pandas as pd
import spacy
import sys
import os

from src.analise import normalizar_texto, tem_padrao_fixo, tem_nome_pessoa


def processar_arquivo(caminho_entrada=None, caminho_saida=None):
    """Lê arquivo Excel, classifica documentos e salva resultado em CSV."""
    
    if caminho_entrada is None:
        caminho_entrada = os.path.join("dados", "entrada", "AMOSTRA_e-SIC.xlsx")
    if caminho_saida is None:
        caminho_saida = os.path.join("dados", "saida", "resultado_analise.csv")
    
    print("Carregando modelo de IA...")
    try:
        nlp = spacy.load("pt_core_news_lg")
    except OSError:
        print("ERRO: Modelo não encontrado")
        print("Execute: python -m spacy download pt_core_news_lg")
        sys.exit()

    if not os.path.exists(caminho_entrada):
        print(f"ERRO: Arquivo não encontrado: {caminho_entrada}")
        return

    print(f"Processando: {caminho_entrada}")
    
    try:
        df = pd.read_excel(caminho_entrada) 
    except Exception as e:
        print(f"ERRO: {e}")
        return

    resultados = []
    total = len(df)
    
    for index, linha in df.iterrows():
        if index > 0 and index % 100 == 0:
            print(f"  Linha {index}/{total}...")

        try:
            id_pedido = linha['ID']
            texto_original = linha['Texto Mascarado']
            texto = normalizar_texto(texto_original)

        except KeyError as e:
            print(f"ERRO: Coluna não encontrada: {e}")
            print("Esperado: ID, Texto Mascarado")
            return
        
        encontrou_padrao, motivo = tem_padrao_fixo(texto)
        
        classificacao = "PUBLICO"
        justificativa = "Nenhum dado sensível encontrado"

        if encontrou_padrao:
            classificacao = "RESTRITO"
            justificativa = motivo
        elif tem_nome_pessoa(texto, nlp):
            classificacao = "RESTRITO"
            justificativa = "Possível Nome Pessoal (IA)"

        resultados.append({
            'ID': id_pedido,
            'Classificacao': classificacao,
            'Justificativa': justificativa,
        })

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    
    df_saida = pd.DataFrame(resultados)
    df_saida.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
    
    print("Concluído com sucesso!")
    print(f"Resultado: {caminho_saida}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        entrada = sys.argv[1]
        saida = sys.argv[2] if len(sys.argv) > 2 else None
        processar_arquivo(entrada, saida)
    else:
        processar_arquivo()
