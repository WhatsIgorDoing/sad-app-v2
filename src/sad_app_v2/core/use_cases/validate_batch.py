from pathlib import Path
from typing import Dict, List, Tuple

from ..domain import DocumentFile, DocumentStatus, ManifestItem
from ..interfaces import IFileRepository, IManifestRepository


class ValidateBatchUseCase:
    """
    Implementa o Caso de Uso UC-01: Validar Lote de Documentos.
    Orquestra os repositórios para comparar arquivos no disco com um manifesto.
    """

    def __init__(self, manifest_repo: IManifestRepository, file_repo: IFileRepository):
        """
        Inicializa o caso de uso com as dependências (repositórios).
        Isso é Injeção de Dependência.
        """
        self._manifest_repo = manifest_repo
        self._file_repo = file_repo

    def _get_file_base_name(self, file_name: str) -> str:
        """
        Extrai o nome base de um arquivo para correspondência.
        Ex: 'DOC-ABC-123_A.pdf' -> 'DOC-ABC-123'
        Esta é uma implementação simples da RN-NEW-001.
        """
        # Remove a extensão
        name_without_ext = Path(file_name).stem
        # Procura por um sufixo de revisão (ex: _A, _0, _rev1) e o remove
        parts = name_without_ext.split("_")
        if len(parts) > 1:
            # Assume que a última parte pode ser uma revisão, então a remove.
            # Esta lógica pode ser refinada se os códigos puderem ter underscores.
            return "_".join(parts[:-1])
        return name_without_ext

    def execute(
        self, manifest_path: Path, source_directory: Path
    ) -> Tuple[List[DocumentFile], List[DocumentFile]]:
        """
        Executa o fluxo principal do caso de uso.
        """
        # 1. Carrega os dados do manifesto e do sistema de arquivos
        manifest_items = self._manifest_repo.load_from_file(manifest_path)
        disk_files = self._file_repo.list_files(source_directory)

        # 2. Cria um dicionário para busca rápida dos itens do manifesto
        manifest_map: Dict[str, ManifestItem] = {
            item.document_code: item for item in manifest_items
        }

        # 3. Inicializa as listas de resultado
        validated_files: List[DocumentFile] = []
        unrecognized_files: List[DocumentFile] = []

        # 4. Itera sobre os arquivos do disco para validação
        for file in disk_files:
            base_name = self._get_file_base_name(file.path.name)

            # 5. Tenta encontrar a correspondência no manifesto
            matched_item = manifest_map.get(base_name)

            if matched_item:
                # Sucesso: A correspondência foi encontrada
                file.status = DocumentStatus.VALIDATED
                file.associated_manifest_item = matched_item
                validated_files.append(file)
            else:
                # Falha: Nenhuma correspondência encontrada
                file.status = DocumentStatus.UNRECOGNIZED
                unrecognized_files.append(file)

        return validated_files, unrecognized_files
