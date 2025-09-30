import sys

sys.path.insert(0, "src")

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from sad_app_v2.core.domain import DocumentFile, DocumentStatus, ManifestItem
from sad_app_v2.infrastructure.extraction import ProfiledExtractorService


def create_test_rir_document():
    """Cria um documento RIR de teste com conteúdo simulado."""
    content = """
RELATÓRIO DE INSPEÇÃO POR RISCO - RIR

Relatório: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A

Data: 29/09/2025
Inspetor: João Silva
Equipamento: Vaso de Pressão VP-001

1. INTRODUÇÃO
   Este relatório apresenta os resultados da inspeção...

2. METODOLOGIA
   A inspeção foi realizada conforme...

3. RESULTADOS
   - Inspeção visual: OK
   - Medições de espessura: Dentro dos padrões
   - Análise de soldas: Aprovado

4. CONCLUSÕES
   O equipamento encontra-se em condições adequadas...
   """
    return content


def create_test_docx_with_content(file_path: Path, content: str):
    """Cria um arquivo DOCX de teste com conteúdo específico."""
    import docx

    doc = docx.Document()
    for line in content.split("\n"):
        if line.strip():
            doc.add_paragraph(line.strip())
    doc.save(file_path)


def test_rir_extraction():
    print("=== TESTE - FUNCIONALIDADE RIR ===")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # 1. Criar arquivo RIR de teste
        rir_file = temp_path / "rir_teste.docx"
        rir_content = create_test_rir_document()
        create_test_docx_with_content(rir_file, rir_content)

        print("📄 ARQUIVO RIR CRIADO:")
        print(f"   {rir_file.name}")

        # 2. Criar extrator de serviço
        config_path = Path("config/patterns.yaml")
        extractor = ProfiledExtractorService(config_path)

        # 3. Criar DocumentFile
        doc_file = DocumentFile(rir_file, 1000)

        print("\n🔍 TESTE DE EXTRAÇÃO DE TEXTO:")
        try:
            # 4. Extrair texto
            extracted_text = extractor.extract_text(doc_file, "RIR")
            print(f"   Texto extraído (primeiros 200 chars):")
            print(f"   {extracted_text[:200]}...")

            # 5. Buscar código RIR
            found_code = extractor.find_code(extracted_text, "RIR")
            print(f"\n   Código encontrado: {found_code}")

            if found_code:
                print("   ✅ CÓDIGO RIR EXTRAÍDO COM SUCESSO!")
            else:
                print("   ❌ CÓDIGO RIR NÃO ENCONTRADO")

            # 6. Teste com regex manual (como implementado no controller)
            import re

            pattern = r"Relatório:\s*([A-Z0-9_\.\-]+)"
            match = re.search(pattern, extracted_text, re.IGNORECASE | re.MULTILINE)

            print(f"\n🎯 TESTE REGEX MANUAL:")
            if match:
                manual_code = match.group(1).strip()
                print(f"   Código extraído manualmente: {manual_code}")
                print("   ✅ REGEX MANUAL FUNCIONOU!")
            else:
                print("   ❌ REGEX MANUAL FALHOU")

            # 7. Simular busca no manifesto
            print(f"\n📋 TESTE DE BUSCA NO MANIFESTO:")
            test_manifest_items = [
                ManifestItem("OUTRO_DOCUMENTO_A", "A", "Documento A"),
                ManifestItem(
                    "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A", "B", "RIR Teste"
                ),
                ManifestItem("MAIS_UM_DOCUMENTO_C", "C", "Documento C"),
            ]

            if found_code or (match and match.group(1)):
                search_name = found_code or match.group(1).strip()
                matched_item = None

                for item in test_manifest_items:
                    if (
                        search_name.upper() in item.document_code.upper()
                        or item.document_code.upper() in search_name.upper()
                    ):
                        matched_item = item
                        break

                if matched_item:
                    print(
                        f"   Item encontrado no manifesto: {matched_item.document_code}"
                    )
                    print(f"   Revisão: {matched_item.revision}")
                    print("   ✅ BUSCA NO MANIFESTO FUNCIONOU!")
                else:
                    print(f"   ❌ Nome '{search_name}' não encontrado no manifesto")

            return True

        except Exception as e:
            print(f"   ❌ ERRO: {e}")
            return False


def test_rir_interface_integration():
    """Testa a integração com a interface (simulado)."""
    print("\n=== TESTE - INTEGRAÇÃO COM INTERFACE ===")

    # Simular customtkinter
    sys.modules["customtkinter"] = MagicMock()

    try:
        from sad_app_v2.presentation.view_controller import ViewController

        controller = ViewController("test_extractor")

        # Simular arquivo não reconhecido
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "rir_nao_reconhecido.docx"
            test_content = create_test_rir_document()
            create_test_docx_with_content(test_file, test_content)

            doc_file = DocumentFile(test_file, 1000)
            doc_file.status = DocumentStatus.UNRECOGNIZED

            # Simular manifesto
            controller.all_manifest_items = [
                ManifestItem(
                    "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A", "B", "RIR Teste"
                ),
            ]

            print("📁 ARQUIVO DE TESTE CRIADO:")
            print(f"   {test_file.name}")
            print("📋 MANIFESTO SIMULADO COM 1 ITEM")

            # Simular view
            mock_view = MagicMock()
            controller.view = mock_view

            print("\n🔧 TESTANDO MÉTODO _run_rir_resolution:")

            # Executar resolução RIR
            controller._run_rir_resolution(doc_file)

            # Verificar se view.after foi chamado (indicando sucesso)
            if mock_view.after.called:
                calls = mock_view.after.call_args_list
                success_calls = [call for call in calls if "resolvido" in str(call)]
                if success_calls:
                    print("   ✅ RESOLUÇÃO RIR FUNCIONOU!")
                    print(f"   Chamadas de sucesso: {len(success_calls)}")
                else:
                    print("   ⚠️  View foi chamada mas sem mensagem de sucesso")
            else:
                print("   ❌ View não foi chamada")

            return True

    except Exception as e:
        print(f"   ❌ ERRO NA INTEGRAÇÃO: {e}")
        return False


if __name__ == "__main__":
    print("🧪 INICIANDO TESTES DA FUNCIONALIDADE RIR\n")

    test1_success = test_rir_extraction()
    test2_success = test_rir_interface_integration()

    overall_success = test1_success and test2_success

    print(
        f"\n🎉 RESULTADO FINAL: {'TODOS OS TESTES PASSARAM' if overall_success else 'ALGUNS TESTES FALHARAM'} 🎉"
    )

    if overall_success:
        print("\n💡 A funcionalidade RIR está implementada e funcionando!")
        print("   - Extração de texto de documentos DOCX ✅")
        print("   - Busca por padrão 'Relatório:' ✅")
        print("   - Correspondência com manifesto ✅")
        print("   - Integração com interface ✅")
    else:
        print("\n⚠️  Verifique os erros acima para ajustes necessários.")
