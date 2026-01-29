from detector_nomes import extrair_nomes

TEXTOS_TESTE = [
    "Denúncia - e-Ouvidoria ... Em resposta, informar o Número Interno 789321.",
]

print("\n=== TESTE COM DADOS REAIS ===")
for t in TEXTOS_TESTE:
    resultado = extrair_nomes(t)
    print("DETECÇÃO:", [
        {**a, "valor": a["valor"].replace("\n", " ")}
        for a in resultado
    ])
