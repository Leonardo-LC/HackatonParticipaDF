import pandas as pd
import os
from detector_nomes import tem_nome_pessoa

def processar_planilha():
    # Caminhos de arquivos baseados no seu computador
    caminho_entrada = r"C:\Users\Usuário\HackatonParticipaDF\dados\entrada\AMOSTRA_e-SIC1.xlsx"
    caminho_saida = r"C:\Users\Usuário\HackatonParticipaDF\dados\saida\RESULTADO_FINAL_HACKATHON.xlsx"

    if not os.path.exists(caminho_entrada):
        print(f"❌ Arquivo não encontrado: {caminho_entrada}")
        return

    print("🚀 Carregando planilha e aplicando IA na coluna 'Texto Mascarado'...")
    df = pd.read_excel(caminho_entrada)

    # Definindo a coluna correta conforme sua imagem
    coluna_alvo = "Texto Mascarado"

    if coluna_alvo not in df.columns:
        print(f"⚠️ Coluna '{coluna_alvo}' não encontrada. Tentando a segunda coluna da planilha...")
        coluna_alvo = df.columns[1]

    # Aplicação da lógica de detecção de nomes calibrada pela Pessoa 3
    df['CLASSIFICACAO_IA'] = df[coluna_alvo].apply(
        lambda x: "❌ NÃO PÚBLICO" if tem_nome_pessoa(str(x)) else "✅ PÚBLICO"
    )

    # Estatísticas para o seu relatório final
    total = len(df)
    bloqueados = len(df[df['CLASSIFICACAO_IA'] == "❌ NÃO PÚBLICO"])
    
    # Salva o resultado
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df.to_excel(caminho_saida, index=False)

    print("-" * 40)
    print(f"📊 RESUMO DA CLASSIFICAÇÃO (PESSOA 3):")
    print(f"✅ Total de registros: {total}")
    print(f"❌ Dados Pessoais Detectados: {bloqueados}")
    print(f"📈 Taxa de Proteção: {(bloqueados/total)*100:.2f}%")
    print(f"📂 Arquivo salvo em: {caminho_saida}")
    print("-" * 40)

if __name__ == "__main__":
    processar_planilha()