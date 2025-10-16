"""
Teste da funcionalidade de detecção e correção de arquivos sem sufixo

Este script cria um ambiente de teste controlado e executa o fluxo completo
para testar a nova funcionalidade que detecta e corrige arquivos com nomes
corretos mas sem sufixo.
"""

import os
import shutil
import tempfile
from pathlib import Path
import random
import string

from src.sad_app_v2.core.domain import DocumentStatus, ManifestItem
from src.sad_app_v2.core.use_cases.validate_batch import ValidateBatchUseCase
from src.sad_app_v2.presentation.view_controller import ViewController
from src.sad_app_v2.presentation.main_view import MainView


def create_test_environment():
    """Cria um ambiente de teste com arquivos e manifesto."""
    # Criar diretório temporário
    temp_dir = tempfile.mkdtemp()
    print(f"Diretório de teste criado: {temp_dir}")

    # Criar arquivos de teste
    file_paths = []

    # 1. Arquivo com nome correto mas sem sufixo
    file_path1 = Path(temp_dir) / "RIR_TESTE_SEM_SUFIXO.pdf"
    with open(file_path1, "w") as f:
        f.write("Conteúdo de teste para RIR_TESTE_SEM_SUFIXO")
    file_paths.append(file_path1)

    # 2. Arquivo com nome correto e sufixo correto
    file_path2 = Path(temp_dir) / "RIR_TESTE_COM_SUFIXO_0.pdf"
    with open(file_path2, "w") as f:
        f.write("Conteúdo de teste para RIR_TESTE_COM_SUFIXO")
    file_paths.append(file_path2)

    # 3. Arquivo com nome totalmente diferente
    file_path3 = Path(temp_dir) / "ARQUIVO_DESCONHECIDO.pdf"
    with open(file_path3, "w") as f:
        f.write("Conteúdo de teste para arquivo desconhecido")
    file_paths.append(file_path3)

    # Criar itens de manifesto para teste
    manifest_items = [
        ManifestItem(
            document_code="RIR_TESTE_SEM_SUFIXO",
            revision="0",
            title="Documento de teste sem sufixo",
        ),
        ManifestItem(
            document_code="RIR_TESTE_COM_SUFIXO",
            revision="0",
            title="Documento de teste com sufixo",
        ),
        ManifestItem(
            document_code="RIR_OUTRO_DOCUMENTO",
            revision="1",
            title="Outro documento qualquer",
        ),
    ]

    print(f"Arquivos criados:")
    for path in file_paths:
        print(f"  - {path.name}")

    print(f"Itens de manifesto criados:")
    for item in manifest_items:
        print(f"  - {item.document_code} (rev: {item.revision})")

    return temp_dir, file_paths, manifest_items


def test_suffix_correction():
    """Teste principal para validação e correção de arquivos sem sufixo."""
    print("\n=== TESTE DE CORREÇÃO DE ARQUIVOS SEM SUFIXO ===\n")

    # Criar ambiente de teste
    temp_dir, file_paths, manifest_items = create_test_environment()

    try:
        # Executar a validação de lote
        print("\n1. Executando a validação do lote...")
        use_case = ValidateBatchUseCase()
        result = use_case.execute(
            directory_path=Path(temp_dir),
            manifest_items=manifest_items,
            file_pattern="*.pdf",
        )

        # Verificar resultados da validação
        print("\n2. Resultados da validação inicial:")
        print(f"   - Arquivos validados: {len(result.validated_files)}")
        print(f"   - Arquivos não reconhecidos: {len(result.unrecognized_files)}")

        # Verificar se o arquivo sem sufixo foi identificado corretamente
        needs_suffix_files = [
            f
            for f in result.unrecognized_files
            if f.status == DocumentStatus.NEEDS_SUFFIX
        ]

        print("\n3. Verificando arquivos que precisam de sufixo:")
        if needs_suffix_files:
            for file in needs_suffix_files:
                print(f"   ✅ Encontrado: {file.path.name}")
                print(f"      - Status: {file.status}")
                print(
                    f"      - Item associado: {file.associated_manifest_item.document_code}"
                )
        else:
            print("   ❌ Nenhum arquivo identificado como NEEDS_SUFFIX")

        # Simular a correção de um arquivo sem sufixo
        if needs_suffix_files:
            print("\n4. Simulando a correção do arquivo sem sufixo...")
            file = needs_suffix_files[0]

            # Criar uma classe mock para a view
            class MockView:
                def __init__(self):
                    self.logs = []

                def add_log_message(self, message):
                    self.logs.append(message)
                    print(f"   📝 LOG: {message}")

                def after(self, ms, func, *args):
                    func(*args)

                def _update_ui_lists(self):
                    print("   🔄 Interface atualizada")

            # Criar controller mock para teste
            mock_view = MockView()
            controller = ViewController(mock_view)
            controller.unrecognized_files = result.unrecognized_files
            controller.validated_files = result.validated_files
            controller.all_manifest_items = manifest_items

            # Executar a resolução RIR no arquivo que precisa de sufixo
            print("\n5. Executando a correção...")
            controller._run_rir_resolution(file)

            # Verificar resultado final
            print("\n6. Verificando resultado final:")
            print(f"   - Arquivos validados: {len(controller.validated_files)}")
            print(
                f"   - Arquivos não reconhecidos: {len(controller.unrecognized_files)}"
            )

            # Verificar se o arquivo foi movido para a lista correta
            file_found = False
            for file in controller.validated_files:
                if str(file.path.stem).startswith("RIR_TESTE_SEM_SUFIXO_"):
                    file_found = True
                    print(f"   ✅ Arquivo corrigido com sucesso: {file.path.name}")
                    print(f"      - Status: {file.status}")

            if not file_found:
                print("   ❌ Falha: Arquivo não foi corrigido corretamente")

            # Verificar se o arquivo foi renomeado fisicamente
            renamed_file = None
            for file in os.listdir(temp_dir):
                if file.startswith("RIR_TESTE_SEM_SUFIXO_"):
                    renamed_file = file
                    break

            if renamed_file:
                print(f"   ✅ Arquivo renomeado fisicamente: {renamed_file}")
            else:
                print("   ❌ Falha: Arquivo não foi renomeado fisicamente")

    finally:
        # Limpar ambiente de teste
        print("\nLimpando ambiente de teste...")
        shutil.rmtree(temp_dir)
        print("Teste finalizado.")


if __name__ == "__main__":
    test_suffix_correction()
