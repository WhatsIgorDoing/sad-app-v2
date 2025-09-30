#!/usr/bin/env python3
"""
Debug detalhado do problema de extração RIR
"""

import re


def debug_rir_extraction():
    """Debug detalhado para entender o problema"""
    print("=== DEBUG DETALHADO RIR ===")
    print()

    # Texto exato do log do usuário
    text = "Item do Critério de Medição:  3.1.1.1 Código da disciplina:  TUB Código do Relatório:  RIR TAG:  V4540N0SBC-00-NN-014-UCR-01 Relatório:  CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG - RELATÓRIO DE INSPEÇÃO DE ..."

    print("📄 TEXTO COMPLETO:")
    print(f"'{text}'")
    print()

    # Encontrar a posição exata de "Relatório:"
    relatorio_pos = text.find("Relatório:")
    if relatorio_pos >= 0:
        print(f"📍 'Relatório:' encontrado na posição: {relatorio_pos}")

        # Mostrar contexto ao redor
        start = max(0, relatorio_pos - 20)
        end = min(len(text), relatorio_pos + 60)
        context = text[start:end]
        print(f"🔍 Contexto: '{context}'")

        # Mostrar os próximos 50 caracteres após "Relatório:"
        after_relatorio = text[relatorio_pos + 10 : relatorio_pos + 60]
        print(f"➡️ Após 'Relatório:': '{after_relatorio}'")

        # Analisar caractere por caractere
        print("\n📝 ANÁLISE CARACTERE POR CARACTERE (após 'Relatório:'):")
        for i, char in enumerate(after_relatorio[:20]):
            if char == " ":
                print(f"   {i:2d}: [ESPAÇO]")
            elif char == "\t":
                print(f"   {i:2d}: [TAB]")
            elif char == "\n":
                print(f"   {i:2d}: [QUEBRA]")
            elif char == "\r":
                print(f"   {i:2d}: [RETURN]")
            else:
                print(f"   {i:2d}: '{char}'")

    print("\n" + "=" * 50)
    print("🧪 TESTE DE MÚLTIPLOS PADRÕES:")
    print("=" * 50)

    patterns = [
        # Padrão atual
        (
            r"Relatório:\s*([A-Z0-9_\.\-\s]+?)(?:\s*-|\s*$|\r|\n)",
            "Atual (problemático)",
        ),
        # Variações mais específicas
        (r"Relatório:\s+([A-Z0-9_\.]+(?:[A-Z0-9_\.\-]+)*)", "Sem espaços internos"),
        (
            r"Relatório:\s*([A-Z0-9_\.\-]+(?:\s+[A-Z0-9_\.\-]+)*)",
            "Com espaços opcionais",
        ),
        (r"Relatório:\s*([^-\n\r]+?)(?:\s*-|\s*$)", "Qualquer coisa até hífen"),
        (r"Relatório:\s*([A-Z0-9_\.\-\s]*?)(?:-TAG|\s*-|\s*$)", "Específico para TAG"),
        (r"Relatório:\s*([A-Z0-9_\.\-]+(?:_[A-Z0-9_\.\-]+)*)", "Underscores separados"),
        (r"Relatório:\s*([A-Z0-9_\.\-]{3,})", "Mínimo 3 caracteres simples"),
        (
            r"Relatório:\s*([A-Z0-9_\.\-\s]+?)(?:-[A-Z]|\s*-|\s*$)",
            "Para antes de hífen+letra",
        ),
    ]

    for pattern, description in patterns:
        print(f"\n🔍 {description}:")
        print(f"   Padrão: {pattern}")

        try:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                result = match.group(1).strip()
                print(f"   ✅ Resultado: '{result}' ({len(result)} chars)")
            else:
                print(f"   ❌ Nenhuma correspondência")
        except Exception as e:
            print(f"   ❌ Erro no regex: {e}")


def test_expected_patterns():
    """Testa padrões com diferentes formatos esperados"""
    print("\n" + "=" * 50)
    print("🎯 TESTE COM FORMATOS ESPERADOS:")
    print("=" * 50)

    # Diferentes possibilidades baseadas no texto
    test_texts = [
        "Relatório:  CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG - DESCRIÇÃO",
        "Relatório: CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG",
        "Relatório:CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG",
        # O texto real do usuário
        "Item do Critério de Medição:  3.1.1.1 Código da disciplina:  TUB Código do Relatório:  RIR TAG:  V4540N0SBC-00-NN-014-UCR-01 Relatório:  CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG - RELATÓRIO DE INSPEÇÃO DE ...",
    ]

    # Padrão que deve funcionar
    best_pattern = r"Relatório:\s*([A-Z0-9_\.\-]+(?:_[A-Z0-9_\.\-]+)*)"

    print(f"📋 Padrão testado: {best_pattern}")
    print()

    for i, test_text in enumerate(test_texts, 1):
        print(f"🧪 Teste {i}: '{test_text[:60]}...'")
        match = re.search(best_pattern, test_text, re.IGNORECASE | re.MULTILINE)
        if match:
            result = match.group(1).strip()
            print(f"   ✅ Capturou: '{result}'")
        else:
            print(f"   ❌ Não capturou")
        print()


if __name__ == "__main__":
    print("🐛 DEBUG DETALHADO DO PROBLEMA RIR")
    print("=" * 60)

    debug_rir_extraction()
    test_expected_patterns()

    print("\n📋 CONCLUSÕES:")
    print("1. Analisar a estrutura exata do texto")
    print("2. Identificar o padrão correto baseado no contexto")
    print("3. Testar o novo padrão antes de aplicar")
    print("4. Considerar variações de formatação")
