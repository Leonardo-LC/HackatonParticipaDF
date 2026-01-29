import pandas as pd
from detector_nomes import classificar_texto

# lê o Excel
df = pd.read_excel("AMOSTRA_e-SIC.xlsx")

# aplica classificação
df["CLASSIFICACAO"] = df["Texto Mascarado"].apply(classificar_texto)

# resumo
print("Total analisados:", len(df))
print(df["CLASSIFICACAO"].value_counts())

# salva resultado
df.to_excel("resultado_classificado.xlsx", index=False)
