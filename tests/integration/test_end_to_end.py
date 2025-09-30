from pathlib import Path

from src.sad_app_v2.core.use_cases.validate_batch import ValidateBatchUseCase
from src.sad_app_v2.infrastructure.excel_reader import ExcelManifestRepository
from src.sad_app_v2.infrastructure.file_system import FileSystemFileRepository


def test_validate_batch_end_to_end(tmp_path):
    """
    Teste end-to-end que usa implementações reais dos repositórios
    para validar um lote de documentos.
    """
    # Setup: Criar arquivos de teste que correspondem ao manifesto
    (tmp_path / "documento_pid_A.pdf").touch()
    (tmp_path / "documento_rir_B.dwg").touch()
    (tmp_path / "DOC-999-UNKNOWN_C.docx").touch()  # Este não está no manifesto

    # Usar o manifesto de exemplo que já temos
    manifest_path = Path("tests/fixtures/manifesto_exemplo.xlsx")

    # Instanciar as implementações reais
    manifest_repo = ExcelManifestRepository()
    file_repo = FileSystemFileRepository()

    # Criar o caso de uso com as implementações reais
    use_case = ValidateBatchUseCase(manifest_repo=manifest_repo, file_repo=file_repo)

    # Execução
    validated, unrecognized = use_case.execute(
        manifest_path=manifest_path, source_directory=tmp_path
    )

    # Verificação
    assert len(validated) == 2  # documento_pid e documento_rir
    assert len(unrecognized) == 1  # DOC-999-UNKNOWN

    # Verifica os arquivos validados
    validated_codes = {f.associated_manifest_item.document_code for f in validated}
    assert "documento_pid" in validated_codes
    assert "documento_rir" in validated_codes

    # Verifica o arquivo não reconhecido
    assert unrecognized[0].path.name == "DOC-999-UNKNOWN_C.docx"


def test_validate_batch_with_subdirectories(tmp_path):
    """
    Testa se o sistema funciona com arquivos em subdiretórios.
    """
    # Setup: Criar estrutura com subdiretórios
    sub_dir = tmp_path / "subdir"
    sub_dir.mkdir()

    (tmp_path / "documento_pid_A.pdf").touch()
    (sub_dir / "documento_rir_B.dwg").touch()

    manifest_path = Path("tests/fixtures/manifesto_exemplo.xlsx")

    # Usar implementações reais
    manifest_repo = ExcelManifestRepository()
    file_repo = FileSystemFileRepository()
    use_case = ValidateBatchUseCase(manifest_repo, file_repo)

    # Execução
    validated, unrecognized = use_case.execute(manifest_path, tmp_path)

    # Verificação
    assert len(validated) == 2
    assert len(unrecognized) == 0

    # Verifica que arquivos de subdiretórios foram encontrados
    file_paths = {str(f.path) for f in validated}
    assert any("subdir" in path for path in file_paths)
