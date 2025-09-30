#!/usr/bin/env python3
"""
Teste da nova lógica RIR com múltiplas correspondências
"""

import re


def test_new_logic():
    """Testa a nova lógica que pega a correspondência mais longa"""
    print("=== TESTE NOVA LÓGICA RIR ===")
    print()

    # Texto real do usuário
    text = "Item do Critério de Medição:  3.1.1.1 Código da disciplina:  TUB Código do Relatório:  RIR TAG:  V4540N0SBC-00-NN-014-UCR-01 Relatório:  CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG - RELATÓRIO DE INSPEÇÃO DE ..."

    print("📄 TEXTO:")
    print(f"'{text}'")
    print()

    # Novo padrão
    pattern = r"Relatório:\s*([A-Z0-9_\.\-]{4,}(?:_[A-Z0-9_\.\-]+)*)"
    print(f"🔍 PADRÃO: {pattern}")
    print()

    # Buscar todas as correspondências
    matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)

    print(f"🎯 CORRESPONDÊNCIAS ENCONTRADAS: {len(matches)}")
    for i, match in enumerate(matches, 1):
        print(f"   {i}. '{match}' ({len(match)} chars)")
    print()

    if matches:
        # Pegar a mais longa
        longest_match = max(matches, key=len)
        print(f"✅ CORRESPONDÊNCIA MAIS LONGA: '{longest_match}'")
        print(f"📏 Tamanho: {len(longest_match)} caracteres")

        # Simular geração do nome do arquivo
        revision = "A"
        new_filename = f"{longest_match}_{revision}.pdf"
        print(f"📁 Nome do arquivo: '{new_filename}'")

        # Comparar com o problema anterior
        print(f"\n⚡ COMPARAÇÃO:")
        print(f"❌ ANTES: 'RIR_0.pdf' (genérico)")
        print(f"✅ DEPOIS: '{new_filename}' (específico)")

        return longest_match
    else:
        print("❌ Nenhuma correspondência encontrada")
        return None


def test_edge_cases():
    """Testa casos extremos"""
    print("\n" + "=" * 60)
    print("🧪 TESTE CASOS EXTREMOS")
    print("=" * 60)

    test_cases = [
        # Caso com múltiplas ocorrências
        "Código do Relatório: RIR TAG: V123 Relatório: SIMPLE_CODE-DESC Relatório: CZ6_LONG_CODE_WITH_UNDERSCORES_AND_NUMBERS_123-TAG",
        # Caso com apenas códigos curtos
        "Relatório: ABC Relatório: XYZ",
        # Caso sem correspondências válidas
        "Documento sem relatório mencionado aqui",
        # Caso real simplificado
        "Relatório: RIR TAG: V4540N0SBC-00-NN-014-UCR-01 Relatório: CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG",
    ]

    pattern = r"Relatório:\s*([A-Z0-9_\.\-]{4,}(?:_[A-Z0-9_\.\-]+)*)"

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔬 Teste {i}: '{test_case[:60]}...'")
        matches = re.findall(pattern, test_case, re.IGNORECASE | re.MULTILINE)

        if matches:
            longest_match = max(matches, key=len)
            print(f"   ✅ Encontradas {len(matches)} correspondências")
            print(f"   🎯 Mais longa: '{longest_match}' ({len(longest_match)} chars)")

            if len(longest_match) > 3:
                print(f"   ✅ Válida (> 3 chars)")
            else:
                print(f"   ❌ Inválida (<= 3 chars)")
        else:
            print(f"   ❌ Nenhuma correspondência")


if __name__ == "__main__":
    print("🔧 TESTE DA NOVA LÓGICA RIR")
    print("=" * 60)

    result = test_new_logic()
    test_edge_cases()

    print("\n" + "=" * 60)
    print("📋 RESUMO:")
    if result:
        print(f"✅ Nova lógica funcionou!")
        print(f"✅ Extraído: '{result}'")
        print(f"✅ Ignora códigos curtos como 'RIR'")
        print(f"✅ Pega a correspondência mais específica")
    else:
        print("❌ Nova lógica falhou")

    print("\n🎉 TESTE CONCLUÍDO!")
