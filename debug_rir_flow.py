#!/usr/bin/env python3
"""
Debug script para testar o fluxo completo de RIR
"""

import re
from pathlib import Path

# Simulação do texto extraído de um documento RIR
SAMPLE_RIR_TEXT = """
RELATÓRIO DE INSPEÇÃO POR RISCO - RIR

Relatório: CZ6_RNEST_U22_3.1.1.1_TUB_RIR_V2960Q0R9B-00-JJ-017-UCR-02
Data: 29/09/2025
Inspetor: João Silva

Este relatório apresenta os resultados da inspeção...
"""


def test_rir_extraction():
    """Testa a extração de nome RIR do texto"""
    print("=== TESTE DE EXTRAÇÃO RIR ===")
    print(f"📄 Texto de exemplo:")
    print(SAMPLE_RIR_TEXT[:200] + "...")
    print()

    # Teste do padrão atual
    pattern = r"Relatório:\s*([A-Z0-9_\.\-]+)"
    match = re.search(pattern, SAMPLE_RIR_TEXT, re.IGNORECASE | re.MULTILINE)

    print(f"🔍 Padrão testado: {pattern}")
    if match:
        extracted_name = match.group(1).strip()
        print(f"✅ Nome extraído: '{extracted_name}'")
        print(f"📏 Comprimento: {len(extracted_name)}")

        # Simular geração do nome do arquivo
        revision = "A"  # Exemplo de revisão
        file_extension = ".pdf"
        new_filename = f"{extracted_name}_{revision}{file_extension}"

        print(f"📁 Nome do arquivo resultante: '{new_filename}'")
        print(f"📏 Comprimento do nome: {len(new_filename)}")

        return extracted_name
    else:
        print("❌ Nenhum nome extraído!")
        return None


def test_use_case_logic():
    """Simula a lógica do use case para RIR"""
    print("\n=== TESTE LÓGICA USE CASE ===")

    # Simular perfis do patterns.yaml
    profiles = {
        "RIR": {
            "patterns": [
                r"Relatório:\s*([A-Z0-9_\.\-]+)",
                r"Código:\s*([A-Z0-9_\.\-]+)",
                r"([A-Z0-9]+_[A-Z0-9]+_[A-Z0-9]+_[\d\.]+_[A-Z]+_RIR_[A-Z0-9\-]+)",
            ]
        }
    }

    def find_code(text: str, profile_id: str):
        """Simula o método find_code do ProfiledExtractorService"""
        profile = profiles.get(profile_id)
        if not profile or not text:
            return None

        patterns = profile.get("patterns", [])
        for i, pattern in enumerate(patterns):
            print(f"   🔍 Testando padrão {i + 1}: {pattern}")
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                result = match.group(1) if match.groups() else match.group(0)
                print(f"   ✅ Encontrado: '{result}'")
                return result
            else:
                print(f"   ❌ Não encontrado")

        return None

    # Testar extração
    found_code = find_code(SAMPLE_RIR_TEXT, "RIR")

    if found_code:
        print(f"\n🎯 Código encontrado pelo use case: '{found_code}'")

        # Simular sanitização
        sanitized_code = re.sub(r"_[A-Z0-9]$", "", found_code, flags=re.IGNORECASE)
        print(f"🧹 Código sanitizado: '{sanitized_code}'")

        return found_code
    else:
        print("\n❌ Nenhum código encontrado pelo use case!")
        return None


def test_fallback_logic():
    """Testa a lógica de fallback no view_controller"""
    print("\n=== TESTE LÓGICA FALLBACK ===")

    # Se o use case não encontrou, vamos para fallback
    found_code = test_use_case_logic()

    if not found_code:
        print("⚠️  Use case falhou, tentando fallback manual...")

        # Fallback: busca direta por "Relatório:"
        pattern = r"Relatório:\s*([A-Z0-9_\.\-]+)"
        match = re.search(pattern, SAMPLE_RIR_TEXT, re.IGNORECASE | re.MULTILINE)

        if match:
            extracted_name = match.group(1).strip()
            print(f"✅ Fallback encontrou: '{extracted_name}'")
            return extracted_name
        else:
            print("❌ Fallback também falhou!")
            return None
    else:
        print("✅ Use case funcionou, não precisa de fallback")
        return found_code


if __name__ == "__main__":
    print("🚀 INICIANDO DEBUG DO FLUXO RIR")
    print("=" * 50)

    # Teste 1: Extração direta
    direct_result = test_rir_extraction()

    # Teste 2: Lógica do use case
    use_case_result = test_use_case_logic()

    # Teste 3: Lógica de fallback
    fallback_result = test_fallback_logic()

    print("\n" + "=" * 50)
    print("📊 RESUMO DOS RESULTADOS:")
    print(
        f"   Extração direta: {'✅' if direct_result else '❌'} {direct_result or 'Falhou'}"
    )
    print(
        f"   Use case:        {'✅' if use_case_result else '❌'} {use_case_result or 'Falhou'}"
    )
    print(
        f"   Fallback:        {'✅' if fallback_result else '❌'} {fallback_result or 'Falhou'}"
    )

    if direct_result and use_case_result and direct_result == use_case_result:
        print("\n🎉 TUDO FUNCIONANDO CORRETAMENTE!")
    else:
        print("\n⚠️  HÁ DIFERENÇAS NO COMPORTAMENTO!")
