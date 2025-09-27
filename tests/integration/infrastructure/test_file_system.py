# tests/integration/infrastructure/test_file_system.py

from src.sad_app_v2.infrastructure.file_system import FileSystemFileRepository


def test_list_files_finds_all_files(tmp_path):
    """
    Verifica se o repositório encontra arquivos na raiz e em subdiretórios.

    Args:
        tmp_path: Uma fixture do pytest que fornece um diretório temporário.
    """
    # Setup: Criar uma estrutura de arquivos de teste
    (tmp_path / "file1.pdf").touch()
    (tmp_path / "file2.docx").touch()

    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "file3.txt").touch()

    repo = FileSystemFileRepository()

    # Execução
    files = repo.list_files(tmp_path)

    # Verificação
    assert len(files) == 3

    # Converte os paths para strings para facilitar a verificação
    file_names = {f.path.name for f in files}
    assert "file1.pdf" in file_names
    assert "file2.docx" in file_names
    assert "file3.txt" in file_names
