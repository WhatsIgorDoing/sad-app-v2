import sys

sys.path.insert(0, "src")

from sad_app_v2.core.use_cases.organize_lots import _get_filename_with_revision


def test_revision_logic():
    print("=== TESTE - LÓGICA DE REVISÃO ===")

    test_cases = [
        # (nome_original, revisão, resultado_esperado, descrição)
        ("documento.pdf", "A", "documento_A.pdf", "Arquivo sem revisão - adicionar"),
        (
            "documento_A.pdf",
            "A",
            "documento_A.pdf",
            "Arquivo já tem revisão A - não duplicar",
        ),
        (
            "documento_B.pdf",
            "A",
            "documento_B_A.pdf",
            "Arquivo tem revisão B, precisar revisar para A",
        ),
        (
            "documento_0.xlsx",
            "0",
            "documento_0.xlsx",
            "Arquivo já tem revisão 0 - não duplicar",
        ),
        (
            "documento.docx",
            "1",
            "documento_1.docx",
            "Arquivo sem revisão - adicionar numérica",
        ),
        (
            "arquivo_sem_extensao",
            "A",
            "arquivo_sem_extensao_A",
            "Arquivo sem extensão - adicionar",
        ),
        (
            "arquivo_sem_extensao_A",
            "A",
            "arquivo_sem_extensao_A",
            "Arquivo sem extensão já com revisão",
        ),
        (
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067.pdf",
            "A",
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067_A.pdf",
            "Nome complexo sem revisão",
        ),
        (
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067_A.pdf",
            "A",
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067_A.pdf",
            "Nome complexo já com revisão A",
        ),
    ]

    print("📋 CASOS DE TESTE:")
    all_passed = True

    for original, revision, expected, description in test_cases:
        result = _get_filename_with_revision(original, revision)
        status = "✅" if result == expected else "❌"

        print(f"\n{status} {description}")
        print(f"   Original: {original}")
        print(f"   Revisão: {revision}")
        print(f"   Esperado: {expected}")
        print(f"   Resultado: {result}")

        if result != expected:
            all_passed = False
            print(f"   ❌ FALHA!")

    print(f"\n{'=' * 50}")
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ A lógica de revisão está funcionando corretamente")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("🔧 Revisar a lógica de detecção de revisão")

    return all_passed


if __name__ == "__main__":
    success = test_revision_logic()
    print(f"\nResultado: {'SUCESSO' if success else 'FALHA'}")
