import sys

sys.path.insert(0, "src")

import shutil
import tempfile
from pathlib import Path

from sad_app_v2.core.domain import DocumentFile, DocumentGroup, ManifestItem
from sad_app_v2.infrastructure.file_system import SafeFileSystemManager
from sad_app_v2.infrastructure.template_filler import OpenpyxlTemplateFiller


def test_real_scenario_with_existing_revisions():
    print("=== TESTE CENÁRIO REAL - ARQUIVOS COM REVISÕES EXISTENTES ===")

    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()
        output_dir.mkdir()

        # 1. Criar arquivos de teste simulando nomes reais com revisões já existentes
        test_files = [
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067_A.pdf",  # Já tem revisão A
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067.xlsx",  # Sem revisão
            "documento_pid_B.docx",  # Já tem revisão B
            "documento_pid.pdf",  # Sem revisão
        ]

        # Criar arquivos físicos de teste
        for filename in test_files:
            test_file = source_dir / filename
            test_file.write_text(f"Conteúdo de {filename}")

        print("📁 ARQUIVOS CRIADOS:")
        for filename in test_files:
            print(f"   {filename}")

        # 2. Criar dados de manifesto
        manifest_items = [
            ManifestItem(
                document_code="CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067",
                revision="A",  # Revisão A no manifesto
                title="Relatório de Teste 1",
                metadata={
                    "FORMATO": "A4",
                    "DISCIPLINA": "CIVIL",
                    "TIPO DE DOCUMENTO": "RIR",
                    "PROPÓSITO": "TESTE",
                    "CAMINHO DATABOOK": "TESTE",
                },
            ),
            ManifestItem(
                document_code="documento_pid",
                revision="B",  # Revisão B no manifesto
                title="Documento PID de Teste",
                metadata={
                    "FORMATO": "A4",
                    "DISCIPLINA": "PROCESSO",
                    "TIPO DE DOCUMENTO": "PID",
                    "PROPÓSITO": "TESTE",
                    "CAMINHO DATABOOK": "TESTE",
                },
            ),
        ]

        # 3. Criar grupos de documentos
        groups = []

        # Grupo 1: Arquivo já com revisão A correta + arquivo sem revisão
        files_group1 = [
            DocumentFile(
                source_dir / test_files[0],
                1000,
                associated_manifest_item=manifest_items[0],
            ),  # Já tem _A
            DocumentFile(
                source_dir / test_files[1],
                1500,
                associated_manifest_item=manifest_items[0],
            ),  # Sem revisão
        ]
        groups.append(
            DocumentGroup(
                document_code=manifest_items[0].document_code, files=files_group1
            )
        )

        # Grupo 2: Arquivo com revisão B (diferente do manifesto) + arquivo sem revisão
        files_group2 = [
            DocumentFile(
                source_dir / test_files[2],
                800,
                associated_manifest_item=manifest_items[1],
            ),  # Tem _B, precisa _B
            DocumentFile(
                source_dir / test_files[3],
                900,
                associated_manifest_item=manifest_items[1],
            ),  # Sem revisão
        ]
        groups.append(
            DocumentGroup(
                document_code=manifest_items[1].document_code, files=files_group2
            )
        )

        # 4. Simular organização (criar estrutura de lote)
        lote_dir = output_dir / "LOTE_TESTE"
        lote_dir.mkdir()

        file_manager = SafeFileSystemManager()

        print(f"\n📋 SIMULANDO MOVIMENTAÇÃO:")
        moved_files = []

        for group in groups:
            print(f"\nGrupo: {group.document_code}")
            for file in group.files:
                manifest_item = file.associated_manifest_item
                revision = manifest_item.revision

                # Usar a lógica nova
                from sad_app_v2.core.use_cases.organize_lots import (
                    _get_filename_with_revision,
                )

                new_filename = _get_filename_with_revision(file.path.name, revision)

                destination = lote_dir / new_filename

                print(f"   {file.path.name} → {new_filename}")
                print(f"     Revisão do manifesto: {revision}")
                print(
                    f"     Arquivo já tinha revisão: {'Sim' if f'_{revision}' in file.path.name else 'Não'}"
                )

                # Mover arquivo
                file_manager.copy_file(file.path, destination)
                moved_files.append(new_filename)

        # 5. Verificar resultado
        print(f"\n📊 RESULTADO FINAL:")
        print(f"   Diretório do lote: {lote_dir}")

        actual_files = [f.name for f in lote_dir.iterdir() if f.is_file()]
        print(f"   Arquivos no lote: {sorted(actual_files)}")

        # 6. Verificações específicas
        expected_files = [
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067_A.pdf",  # Não mudou
            "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_BSE-BA-02-022-DKF-0067_A.xlsx",  # Adicionou _A
            "documento_pid_B.docx",  # Não mudou (já tinha _B)
            "documento_pid_B.pdf",  # Adicionou _B
        ]

        print(f"\n🔍 VERIFICAÇÕES:")
        all_correct = True
        for expected in expected_files:
            if expected in actual_files:
                print(f"   ✅ {expected}")
            else:
                print(f"   ❌ {expected} (não encontrado)")
                all_correct = False

        # Verificar se não há duplicações
        no_duplicates = len(actual_files) == len(set(actual_files))
        print(f"   {'✅' if no_duplicates else '❌'} Sem duplicações")

        return all_correct and no_duplicates


if __name__ == "__main__":
    success = test_real_scenario_with_existing_revisions()
    print(f"\n🎉 RESULTADO: {'SUCESSO COMPLETO' if success else 'FALHA'} 🎉")
