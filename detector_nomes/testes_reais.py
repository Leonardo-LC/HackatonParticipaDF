import pandas as pd
import os
from detector_nomes import extrair_nomes

# Testes manuais primeiro
TEXTOS_TESTE = [
    "Denúncia - e-Ouvidoria ... Em resposta, informar o Número Interno 789321.",
    "O senhor João da Silva solicitou informações sobre sua conta.",
    "Moro na Quadra 3, Lote 10 - Brasília.",
    "Maria Oliveira enviou documento em 2024.",
    "A Secretaria de Saúde do DF respondeu.",
    "Me chamo Braga, preciso de ajuda urgente.",
]

print("=" * 60)
print("=== TESTE COM EXEMPLOS MANUAIS ===")
print("=" * 60)
for i, t in enumerate(TEXTOS_TESTE, 1):
    resultado = extrair_nomes(t)
    print(f"\n[{i}] TEXTO: {t[:70]}...")
    if resultado:
        print(f"    ✓ DETECTADO: {[r['valor'] for r in resultado]}")
    else:
        print(f"    ✗ Nenhum nome detectado")

# Agora testa com dados reais do arquivo Excel
print("\n" + "=" * 60)
print("=== TESTE COM DADOS REAIS DO ARQUIVO ===")
print("=" * 60)

caminho_entrada = os.path.join("..", "dados", "entrada", "AMOSTRA_e-SIC.xlsx")

if os.path.exists(caminho_entrada):
    try:
        df = pd.read_excel(caminho_entrada)
        print(f"\n✓ Arquivo encontrado: {caminho_entrada}")
        print(f"✓ Total de linhas: {len(df)}")
        
        coluna_alvo = 'Texto Mascarado'
        if coluna_alvo not in df.columns:
            print(f"✗ Coluna '{coluna_alvo}' não encontrada!")
            print(f"  Colunas disponíveis: {list(df.columns)}")
        else:
            encontrados = 0
            nao_encontrados = 0
            
            print(f"\nAnalisando primeiras 20 linhas...\n")
            
            for idx, (index, linha) in enumerate(df.iterrows()):
                if idx >= 20:  # Limita a 20 primeiras para não sobrecarregar
                    break
                    
                id_pedido = linha.get('ID', f'linha_{idx}')
                texto = str(linha[coluna_alvo])
                
                resultado = extrair_nomes(texto)
                
                if resultado:
                    encontrados += 1
                    nomes = [r['valor'] for r in resultado]
                    print(f"[ID {id_pedido}] ✓ ENCONTRADO: {nomes}")
                else:
                    nao_encontrados += 1
            
            print(f"\n" + "-" * 60)
            print(f"Resumo (primeiras 20 linhas):")
            print(f"  ✓ Linhas com nomes detectados: {encontrados}")
            print(f"  ✗ Linhas sem nomes: {nao_encontrados}")
            print(f"  Taxa de detecção: {(encontrados/(encontrados+nao_encontrados)*100):.1f}%")
            
    except Exception as e:
        print(f"✗ Erro ao ler arquivo: {e}")
else:
    print(f"✗ Arquivo não encontrado: {caminho_entrada}")
    print(f"  Caminho esperado: {os.path.abspath(caminho_entrada)}")
