# src/sad_app_v2/infrastructure/file_system.py

from pathlib import Path
from typing import List

from ..core.domain import DocumentFile
from ..core.interfaces import IFileRepository, SourceDirectoryNotFoundError


class FileSystemFileRepository(IFileRepository):
    """Implementação concreta que lista arquivos de um diretório no disco."""

    def list_files(self, directory: Path) -> List[DocumentFile]:
        if not directory.is_dir():
            raise SourceDirectoryNotFoundError(f"Diretório não encontrado: {directory}")

        found_files: List[DocumentFile] = []

        # .rglob('*') busca recursivamente por todos os arquivos
        for path in directory.rglob("*"):
            if path.is_file():
                found_files.append(
                    DocumentFile(path=path, size_bytes=path.stat().st_size)
                )
        return found_files
