import sys

sys.path.insert(0, "src")

import re
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

# Simular customtkinter
sys.modules["customtkinter"] = MagicMock()

from sad_app_v2.core.domain import DocumentFile, DocumentStatus, ManifestItem
from sad_app_v2.presentation.view_controller import ViewController


def test_rir_extraction_debug():
    print("=== DEBUG - EXTRAÇÃO DE NOME RIR ===")

    # 1. Testar regex diretamente
    test_content = """
RELATÓRIO DE INSPEÇÃO POR RISCO - RIR

Relatório: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A

Data: 29/09/2025
Inspetor: João Silva
    """

    print("📄 CONTEÚDO DE TESTE:")
    print(test_content)

    print("\n🔍 TESTANDO REGEX:")
    pattern = r"Relatório:\s*([A-Z0-9_\.\-]+)"
    match = re.search(pattern, test_content, re.IGNORECASE | re.MULTILINE)

    if match:
        extracted_name = match.group(1).strip()
        print(f"   ✅ Nome extraído: '{extracted_name}'")
        print(f"   Comprimento: {len(extracted_name)}")
        print(f"   Tipo: {type(extracted_name)}")
    else:
        print("   ❌ Regex não encontrou correspondência")
        return False

    # 2. Testar com diferentes variações do padrão
    print("\n🧪 TESTANDO VARIAÇÕES:")

    variations = [
        "Relatório: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A",
        "Relatório:CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A",
        "relatório: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A",
        "RELATÓRIO: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A",
    ]

    for variation in variations:
        match = re.search(pattern, variation, re.IGNORECASE | re.MULTILINE)
        if match:
            result = match.group(1).strip()
            print(f"   ✅ '{variation}' → '{result}'")
        else:
            print(f"   ❌ '{variation}' → Não encontrado")

    # 3. Testar função completa com mock
    print("\n🔧 TESTANDO FUNÇÃO COMPLETA:")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_file = temp_path / "teste_rir.pdf"
        test_file.write_text("arquivo simulado")

        # Configurar controller
        controller = ViewController("test_extractor")

        # Mock do extrator
        mock_extractor = MagicMock()
        mock_extractor.extract_text.return_value = test_content
        controller.extractor_service = mock_extractor

        # Mock da view
        mock_view = MagicMock()
        controller.view = mock_view

        # Manifesto de teste
        controller.all_manifest_items = [
            ManifestItem("CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A", "B", "RIR Teste")
        ]

        # Arquivo de teste
        doc_file = DocumentFile(test_file, 1000)
        controller.unrecognized_files = [doc_file]
        controller.validated_files = []

        print(f"   Arquivo original: {test_file.name}")
        print(f"   Conteúdo mock: {test_content[:50]}...")

        # Executar resolução
        try:
            controller._run_rir_resolution(doc_file)

            # Verificar resultado
            expected_name = "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A_B.pdf"
            expected_path = temp_path / expected_name

            print(f"   Nome esperado: {expected_name}")
            print(f"   Arquivo renomeado existe: {expected_path.exists()}")

            if expected_path.exists():
                print("   ✅ RENOMEAÇÃO FUNCIONOU!")

                # Verificar lista de validados
                if controller.validated_files:
                    validated = controller.validated_files[0]
                    print(f"   ✅ Arquivo validado: {validated.path.name}")
                    print(
                        f"   ✅ Document code: {validated.manifest_item.document_code}"
                    )
                    return True
            else:
                print("   ❌ RENOMEAÇÃO FALHOU")
                # Listar arquivos no diretório
                files = list(temp_path.iterdir())
                print(f"   Arquivos no diretório: {[f.name for f in files]}")
                return False

        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            import traceback

            traceback.print_exc()
            return False


def test_regex_patterns():
    """Testa diferentes padrões regex para capturar o nome após Relatório:"""
    print("\n=== TESTE - PADRÕES REGEX ===")

    test_texts = [
        "Relatório: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A",
        "Relatório:CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A",
        "Relatório: ABC_DEF_123-456",
        "Relatório: TESTE_MUITO_LONGO_COM_NUMEROS_123.456.789_ABC-DEF",
    ]

    patterns = [
        r"Relatório:\s*([A-Z0-9_\.\-]+)",  # Atual
        r"Relatório:\s*([A-Z0-9_\.\-\s]+)",  # Com espaços
        r"Relatório:\s*([^\s\n\r]+)",  # Qualquer coisa que não seja espaço
        r"Relatório:\s*(.+?)(?:\s|$)",  # Até próximo espaço ou fim
    ]

    for i, pattern in enumerate(patterns, 1):
        print(f"\n🔍 PADRÃO {i}: {pattern}")
        for text in test_texts:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                result = match.group(1).strip()
                print(f"   '{text}' → '{result}'")
            else:
                print(f"   '{text}' → ❌ Não encontrado")


if __name__ == "__main__":
    print("🐛 DEBUG - PROBLEMA DE RENOMEAÇÃO RIR\n")

    test1_success = test_rir_extraction_debug()
    test_regex_patterns()

    print(
        f"\n🎯 RESULTADO DEBUG: {'Funcionando' if test1_success else 'Problema identificado'}"
    )

    if not test1_success:
        print("\n💡 POSSÍVEIS CAUSAS:")
        print("   1. Regex não está capturando o nome corretamente")
        print("   2. Variável extracted_name está sendo sobrescrita")
        print("   3. Problema na lógica de renomeação do arquivo")
        print("   4. Mock não está simulando a extração corretamente")
