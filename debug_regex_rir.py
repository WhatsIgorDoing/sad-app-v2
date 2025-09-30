import re


def test_regex_patterns():
    print("=== DEBUG - PADRÕES REGEX PARA RIR ===")

    # Exemplo real fornecido pelo usuário
    test_content = """
RELATÓRIO DE INSPEÇÃO POR RISCO - RIR

Relatório: CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02

Data: 29/09/2025
Inspetor: João Silva
    """

    print("📄 CONTEÚDO DE TESTE:")
    print(test_content)

    # Diferentes padrões para testar
    patterns = [
        # Padrão atual (pode estar limitado)
        r"Relatório:\s*([A-Z0-9_\.\-]+)",
        # Padrão mais permissivo para caracteres
        r"Relatório:\s*([A-Z0-9_\.\-\s]+)",
        # Padrão que captura até quebra de linha
        r"Relatório:\s*([^\r\n]+)",
        # Padrão que captura tudo exceto espaços em branco no final
        r"Relatório:\s*(.+?)(?:\s*$|\s*\n)",
        # Padrão específico para códigos longos com hífens
        r"Relatório:\s*([A-Z0-9_\.\-]+(?:-[A-Z0-9]+)*)",
        # Padrão muito permissivo
        r"Relatório:\s*(.+)",
    ]

    pattern_names = [
        "Atual (limitado)",
        "Com espaços",
        "Até quebra de linha",
        "Até fim/quebra",
        "Com múltiplos hífens",
        "Muito permissivo",
    ]

    expected_result = "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02"

    print(f"\n🎯 RESULTADO ESPERADO: '{expected_result}'")
    print(f"📏 Comprimento esperado: {len(expected_result)}")

    for i, (pattern, name) in enumerate(zip(patterns, pattern_names), 1):
        print(f"\n🔍 PADRÃO {i} - {name}:")
        print(f"   Regex: {pattern}")

        match = re.search(pattern, test_content, re.IGNORECASE | re.MULTILINE)

        if match:
            result = match.group(1).strip()
            print(f"   ✅ Capturado: '{result}'")
            print(f"   📏 Comprimento: {len(result)}")

            # Verificar se capturou corretamente
            if result == expected_result:
                print(f"   🎉 PERFEITO! Capturou exatamente o esperado")
            elif expected_result in result:
                print(f"   ⚠️  Capturou mais que o esperado")
            elif result in expected_result:
                print(f"   ⚠️  Capturou menos que o esperado")
            else:
                print(f"   ❌ Resultado diferente do esperado")
        else:
            print(f"   ❌ Não encontrou correspondência")

    # Teste com variações do texto
    print(f"\n🧪 TESTE COM VARIAÇÕES:")

    variations = [
        "Relatório: CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02",
        "Relatório:CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02",
        "relatório: CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02",
        "RELATÓRIO: CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02",
        "Relatório: CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02   ",  # Com espaços no final
    ]

    # Testar com o melhor padrão encontrado
    best_pattern = r"Relatório:\s*([^\r\n]+)"  # Até quebra de linha

    for variation in variations:
        match = re.search(best_pattern, variation, re.IGNORECASE | re.MULTILINE)
        if match:
            result = match.group(1).strip()
            print(f"   ✅ '{variation[:30]}...' → '{result}'")
        else:
            print(f"   ❌ '{variation[:30]}...' → Não encontrado")


def test_current_vs_improved():
    print(f"\n=== COMPARAÇÃO: ATUAL vs MELHORADO ===")

    test_names = [
        "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A",  # Exemplo anterior
        "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02",  # Novo exemplo
        "ABC_DEF_123-456-789-GHI",  # Teste com múltiplos hífens
        "TEST_DOCUMENTO_MUITO_LONGO_COM_VARIOS_CARACTERES_123.456.789-ABC-DEF-GHI",  # Teste longo
    ]

    current_pattern = r"Relatório:\s*([A-Z0-9_\.\-]+)"
    improved_pattern = r"Relatório:\s*([^\r\n]+)"

    for name in test_names:
        test_text = f"Relatório: {name}"

        print(f"\n📄 Testando: {name}")

        # Padrão atual
        match_current = re.search(
            current_pattern, test_text, re.IGNORECASE | re.MULTILINE
        )
        current_result = (
            match_current.group(1).strip() if match_current else "NÃO ENCONTRADO"
        )

        # Padrão melhorado
        match_improved = re.search(
            improved_pattern, test_text, re.IGNORECASE | re.MULTILINE
        )
        improved_result = (
            match_improved.group(1).strip() if match_improved else "NÃO ENCONTRADO"
        )

        print(f"   Atual:     '{current_result}'")
        print(f"   Melhorado: '{improved_result}'")

        if current_result == improved_result:
            print(f"   ✅ Ambos iguais")
        elif improved_result == name:
            print(f"   🎉 Melhorado capturou corretamente")
        else:
            print(f"   ⚠️  Resultados diferentes")


if __name__ == "__main__":
    test_regex_patterns()
    test_current_vs_improved()
