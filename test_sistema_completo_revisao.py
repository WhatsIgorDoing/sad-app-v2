import sys

sys.path.insert(0, "src")

import tempfile
from pathlib import Path

from sad_app_v2.core.use_cases.organize_lots import OrganizeAndGenerateLotsUseCase
from sad_app_v2.core.use_cases.validate_batch import ValidateBatchUseCase
from sad_app_v2.infrastructure.excel_reader import ExcelManifestRepository
from sad_app_v2.infrastructure.file_system import (
    FileSystemFileRepository,
    SafeFileSystemManager,
)
from sad_app_v2.infrastructure.services import GreedyLotBalancerService
from sad_app_v2.infrastructure.template_filler import OpenpyxlTemplateFiller


def test_complete_system_with_revision_logic():
    print("=== TESTE SISTEMA COMPLETO - PREVENÇÃO DUPLICAÇÃO REVISÃO ===")

    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = Path(temp_dir) / "source"
        output_dir = Path(temp_dir) / "output"
        source_dir.mkdir()

        # 1. Criar arquivos de teste simulando situação real
        test_files = {
            # Arquivo que já tem a revisão correta
            "documento_pid_A.docx": "A",  # Já tem _A, manifesto tem A
            "documento_pid.pdf": "A",  # Sem revisão, manifesto tem A
            # Arquivo que já tem revisão diferente
            "documento_rir_B.xlsx": "A",  # Tem _B, manifesto tem A (vai virar _B_A)
            "documento_rir.pdf": "A",  # Sem revisão, manifesto tem A
        }

        # Criar arquivos físicos
        for filename, _ in test_files.items():
            (source_dir / filename).write_text(f"Conteúdo de {filename}")

        print("📁 ARQUIVOS DE TESTE CRIADOS:")
        for filename, manifest_revision in test_files.items():
            current_has_revision = "_" in filename.replace(".pdf", "").replace(
                ".docx", ""
            ).replace(".xlsx", "")
            print(f"   {filename}")
            print(f"     Revisão no manifesto: {manifest_revision}")
            print(f"     Já tem revisão: {'Sim' if current_has_revision else 'Não'}")

        # 2. Copiar manifesto e template para local temporário
        import shutil

        temp_manifest = source_dir / "manifesto_exemplo.xlsx"
        temp_template = source_dir / "template_exemplo.xlsx"

        shutil.copy("tests/fixtures/manifesto_exemplo.xlsx", temp_manifest)
        shutil.copy("tests/fixtures/template_exemplo.xlsx", temp_template)

        # 3. Executar validação
        manifest_repo = ExcelManifestRepository()
        file_repo = FileSystemFileRepository()

        validate_uc = ValidateBatchUseCase(manifest_repo, file_repo)

        try:
            validated_files, unrecognized = validate_uc.execute(
                temp_manifest, source_dir
            )

            print(f"\n📋 VALIDAÇÃO:")
            print(f"   Arquivos validados: {len(validated_files)}")
            print(f"   Arquivos não reconhecidos: {len(unrecognized)}")

            if validated_files:
                # 4. Executar organização
                balancer = GreedyLotBalancerService()
                file_manager = SafeFileSystemManager()
                template_filler = OpenpyxlTemplateFiller(file_manager)

                organize_uc = OrganizeAndGenerateLotsUseCase(
                    balancer, file_manager, template_filler
                )

                result = organize_uc.execute(
                    validated_files=validated_files,
                    output_directory=output_dir,
                    master_template_path=temp_template,
                    max_docs_per_lot=10,
                    start_sequence_number=1,
                    lot_name_pattern="LOTE_XXXX",
                )

                print(f"\n📊 ORGANIZAÇÃO:")
                print(f"   Sucesso: {result.success}")
                print(f"   Lotes criados: {result.lots_created}")
                print(f"   Arquivos movidos: {result.files_moved}")

                if result.success:
                    # 5. Verificar resultado
                    lote_dir = output_dir / "LOTE_0001"
                    if lote_dir.exists():
                        files_in_lot = [
                            f.name
                            for f in lote_dir.iterdir()
                            if f.is_file() and not f.name.endswith(".xlsx")
                        ]

                        print(f"\n🎯 ARQUIVOS NO LOTE:")
                        for file in sorted(files_in_lot):
                            print(f"   {file}")

                        # Verificar se a lógica de revisão funcionou
                        revision_logic_working = True

                        print(f"\n🔍 VERIFICAÇÃO DA LÓGICA DE REVISÃO:")

                        # Casos esperados:
                        expected_results = {
                            "documento_pid_A.docx": "documento_pid_A.docx",  # Não muda
                            "documento_pid.pdf": "documento_pid_A.pdf",  # Adiciona _A
                            "documento_rir_B.xlsx": "documento_rir_B_A.xlsx",  # Adiciona _A
                            "documento_rir.pdf": "documento_rir_A.pdf",  # Adiciona _A
                        }

                        for original, expected in expected_results.items():
                            if expected in files_in_lot:
                                print(f"   ✅ {original} → {expected}")
                            else:
                                print(f"   ❌ {original} → {expected} (não encontrado)")
                                revision_logic_working = False

                        return revision_logic_working
                    else:
                        print(f"   ❌ Diretório do lote não encontrado")
                        return False
                else:
                    print(f"   ❌ Organização falhou: {result.message}")
                    return False
            else:
                print("   ❌ Nenhum arquivo foi validado")
                return False

        except Exception as e:
            print(f"   ❌ Erro na validação: {e}")
            return False


if __name__ == "__main__":
    success = test_complete_system_with_revision_logic()
    print(
        f"\n🎊 RESULTADO FINAL: {'SISTEMA PERFEITO' if success else 'NECESSITA AJUSTES'} 🎊"
    )
