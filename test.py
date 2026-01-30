"""Validação do sistema de classificação."""

import spacy
from src.analise import normalizar_texto, tem_padrao_fixo, tem_nome_pessoa

print("Carregando modelo...")
nlp = spacy.load("pt_core_news_lg")

testes = [
    ("Sem dados sensíveis", False),
    ("CPF: 123.456.789-10", True),
    ("Email: teste@example.com", True),
    ("Telefone: (11) 98765-4321", True),
    ("João da Silva solicitou", True),
    ("Secretaria de Saúde", False),
]

print("\nValidando detecção:\n")
passed = 0

for texto, esperado in testes:
    encontrou_padrao, _ = tem_padrao_fixo(texto)
    tem_nome = tem_nome_pessoa(texto, nlp)
    detectou = encontrou_padrao or tem_nome
    
    status = "✓" if detectou == esperado else "✗"
    print(f"{status} {texto[:50]}... → {'RESTRITO' if detectou else 'PUBLICO'}")
    
    if detectou == esperado:
        passed += 1

print(f"\nResultado: {passed}/{len(testes)} testes passaram")
