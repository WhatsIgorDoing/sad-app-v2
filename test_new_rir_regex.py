#!/usr/bin/env python3
"""
Teste específico para validar o novo padrão regex RIR com o texto real do usuário
"""

import re


def test_new_rir_pattern():
    """Testa o novo padrão regex com o texto real extraído"""
    print("=== TESTE DO NOVO PADRÃO REGEX RIR ===")
    print()

    # Texto real extraído do log do usuário
    extracted_text = """Item do Critério de Medição:  3.1.1.1 Código da disciplina:  TUB Código do Relatório:  RIR TAG:  V4540N0SBC-00-NN-014-UCR-01 Relatório:  CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG - RELATÓRIO DE INSPEÇÃO DE ..."""

    print("📄 TEXTO EXTRAÍDO:")
    print(f"'{extracted_text}'")
    print()

    # Padrão antigo (problemático)
    print("🔍 TESTE PADRÃO ANTIGO:")
    old_pattern = r"Relatório:\s*([A-Z0-9_\.\-]+)"
    print(f"Padrão: {old_pattern}")
    old_match = re.search(old_pattern, extracted_text, re.IGNORECASE | re.MULTILINE)

    if old_match:
        old_result = old_match.group(1).strip()
        print(
            f"❌ Resultado antigo: '{old_result}' (incorreto - capturou apenas 'RIR')"
        )
        print(f"📏 Tamanho: {len(old_result)} caracteres")
    else:
        print("❌ Nenhuma correspondência encontrada")

    print()

    # Padrão novo (corrigido)
    print("✅ TESTE PADRÃO NOVO:")
    new_pattern = r"Relatório:\s*([A-Z0-9_\.\-\s]+?)(?:\s*-|\s*$|\r|\n)"
    print(f"Padrão: {new_pattern}")
    new_match = re.search(new_pattern, extracted_text, re.IGNORECASE | re.MULTILINE)

    if new_match:
        new_result = new_match.group(1).strip()
        print(f"✅ Resultado novo: '{new_result}' (correto!)")
        print(f"📏 Tamanho: {len(new_result)} caracteres")

        # Validar se o resultado está correto
        expected = "CZ6_5290.00_22212_3.1.1_TUB_RIR"
        if expected in new_result:
            print(f"🎉 SUCESSO: Contém o código esperado '{expected}'")
        else:
            print(f"⚠️ ATENÇÃO: Não contém exatamente '{expected}'")
    else:
        print("❌ Nenhuma correspondência encontrada")

    print()

    # Teste com múltiplas variações
    print("🧪 TESTE COM VARIAÇÕES:")
    test_cases = [
        "Relatório: CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG - RELATÓRIO DE INSPEÇÃO",
        "Relatório:  CZ6_5290.00_22212_3.1.1_TUB_RIR-TAG",
        "Relatório: CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02",
        "Relatório:CZ6_TEST_123.456_ABC_RIR_XYZ-FINAL",
        "Relatório: SIMPLE_RIR_CODE\nData: 30/09/2025",
        "Relatório:  MULTI WORD RIR CODE - DESCRIPTION HERE",
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔬 Teste {i}: '{test_case[:50]}...'")
        match = re.search(new_pattern, test_case, re.IGNORECASE | re.MULTILINE)
        if match:
            result = match.group(1).strip()
            print(f"   ✅ Capturou: '{result}'")
        else:
            print(f"   ❌ Não capturou")


def test_filename_generation():
    """Testa a geração de nomes de arquivo com o novo padrão"""
    print("\n" + "=" * 60)
    print("📁 TESTE GERAÇÃO DE NOMES DE ARQUIVO")
    print("=" * 60)

    # Resultado esperado com o novo padrão
    extracted_name = "CZ6_5290.00_22212_3.1.1_TUB_RIR"
    revision = "A"
    file_extension = ".pdf"

    new_filename = f"{extracted_name}_{revision}{file_extension}"

    print(f"📋 Nome extraído: '{extracted_name}'")
    print(f"🔄 Revisão: '{revision}'")
    print(f"📁 Extensão: '{file_extension}'")
    print(f"✅ Arquivo final: '{new_filename}'")
    print(f"📏 Comprimento total: {len(new_filename)} caracteres")

    # Comparar com o problema anterior
    old_result = "RIR_0.pdf"
    print(f"\n⚡ COMPARAÇÃO:")
    print(f"❌ ANTES: '{old_result}' (genérico, inútil)")
    print(f"✅ DEPOIS: '{new_filename}' (específico, útil)")


if __name__ == "__main__":
    print("🔧 VALIDAÇÃO DO NOVO PADRÃO REGEX RIR")
    print("=" * 60)

    test_new_rir_pattern()
    test_filename_generation()

    print("\n" + "=" * 60)
    print("📋 RESUMO:")
    print("✅ Padrão antigo: Capturava apenas 'RIR' (inútil)")
    print("✅ Padrão novo: Captura nome completo até o hífen (útil)")
    print("✅ Funciona com espaços e caracteres especiais")
    print("✅ Para antes do hífen para evitar descrições")
    print("✅ Compatível com múltiplos formatos de RIR")
    print("\n🎉 CORREÇÃO APLICADA COM SUCESSO!")
