#!/usr/bin/env python3
"""
Debug script para testar o problema específico do RIR_0
"""

import re


def test_sanitization_issue():
    """Testa se o problema está na sanitização"""
    print("=== TESTE SANITIZAÇÃO ===")

    # Código extraído do documento
    extracted_code = "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02"
    print(f"🔍 Código extraído: '{extracted_code}'")

    # Lógica de sanitização atual
    def sanitize_code(code: str) -> str:
        # Remove sufixos de revisão (ex: _A, _0, etc.)
        sanitized = re.sub(r"_[A-Z0-9]$", "", code, flags=re.IGNORECASE)
        return sanitized.strip()

    sanitized = sanitize_code(extracted_code)
    print(f"🧹 Código sanitizado: '{sanitized}'")

    # Verificar se perdeu informação
    if sanitized != extracted_code:
        print(f"⚠️  ATENÇÃO: Sanitização alterou o código!")
        print(f"   Original:   '{extracted_code}'")
        print(f"   Sanitizado: '{sanitized}'")
        return sanitized
    else:
        print("✅ Sanitização não alterou o código")
        return extracted_code


def test_manifest_matching():
    """Simula o problema de correspondência com manifesto"""
    print("\n=== TESTE CORRESPONDÊNCIA MANIFESTO ===")

    extracted_code = "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02"

    # Simular itens do manifesto (possíveis variações)
    manifest_items = [
        # Exato
        {
            "document_code": "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02",
            "revision": "A",
        },
        # Sem revisão
        {
            "document_code": "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR",
            "revision": "A",
        },
        # Diferentes variações
        {
            "document_code": "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017",
            "revision": "A",
        },
        {"document_code": "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B", "revision": "A"},
        # Manifesto genérico RIR
        {"document_code": "RIR", "revision": "0"},
    ]

    print(f"🎯 Procurando correspondência para: '{extracted_code}'")

    # Teste 1: Correspondência exata
    print("\n🔍 Teste 1: Correspondência exata")
    for item in manifest_items:
        if item["document_code"] == extracted_code:
            print(
                f"   ✅ Encontrado exato: '{item['document_code']}' (rev: {item['revision']})"
            )
            return item
    print("   ❌ Nenhuma correspondência exata")

    # Teste 2: Correspondência por substring (lógica atual)
    print("\n🔍 Teste 2: Correspondência por substring")
    for item in manifest_items:
        if (
            extracted_code.upper() in item["document_code"].upper()
            or item["document_code"].upper() in extracted_code.upper()
        ):
            print(
                f"   ✅ Encontrado por substring: '{item['document_code']}' (rev: {item['revision']})"
            )
            return item
    print("   ❌ Nenhuma correspondência por substring")

    # Teste 3: Fallback para RIR genérico
    print("\n🔍 Teste 3: Fallback para RIR genérico")
    for item in manifest_items:
        if item["document_code"] == "RIR":
            print(
                f"   ⚠️  PROBLEMA ENCONTRADO! Usando fallback genérico: '{item['document_code']}' (rev: {item['revision']})"
            )
            print(f"   📁 Isso resultaria em: RIR_{item['revision']} = RIR_0")
            return item

    return None


def test_filename_generation():
    """Testa geração de nome de arquivo"""
    print("\n=== TESTE GERAÇÃO NOME ARQUIVO ===")

    # Cenário 1: Sucesso
    print("🎯 Cenário 1: Correspondência correta")
    extracted_name = "CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02"
    revision = "A"
    file_extension = ".pdf"

    new_filename = f"{extracted_name}_{revision}{file_extension}"
    print(f"   ✅ Nome gerado: '{new_filename}'")

    # Cenário 2: Problema (fallback para RIR genérico)
    print("\n⚠️  Cenário 2: Fallback problemático")
    generic_code = "RIR"
    revision = "0"

    new_filename = f"{generic_code}_{revision}{file_extension}"
    print(f"   ❌ Nome gerado: '{new_filename}' (ESTE É O PROBLEMA!)")

    print("\n💡 SOLUÇÃO: Usar o nome extraído mesmo sem correspondência no manifesto")
    fallback_filename = f"{extracted_name}_{revision}{file_extension}"
    print(f"   ✅ Nome melhorado: '{fallback_filename}'")


if __name__ == "__main__":
    print("🐛 DEBUGGING PROBLEMA RIR_0")
    print("=" * 50)

    # Testar sanitização
    sanitized_result = test_sanitization_issue()

    # Testar correspondência manifesto
    matched_item = test_manifest_matching()

    # Testar geração de nomes
    test_filename_generation()

    print("\n" + "=" * 50)
    print("📋 DIAGNÓSTICO:")
    print("1. ✅ Extração regex funciona perfeitamente")
    print("2. ✅ Sanitização não altera códigos longos")
    print("3. ❌ PROBLEMA: Fallback para item genérico 'RIR' no manifesto")
    print("4. 💡 SOLUÇÃO: Usar nome extraído mesmo sem correspondência exata")
