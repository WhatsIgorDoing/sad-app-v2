# src/sad_app_v2/infrastructure/template_filler.py

from pathlib import Path
from typing import List

import openpyxl

from ..core.domain import DocumentGroup
from ..core.interfaces import (
    IFileSystemManager,
    ITemplateFiller,
    TemplateFillError,
    TemplateNotFoundError,
)


class OpenpyxlTemplateFiller(ITemplateFiller):
    """Implementação que usa openpyxl para preencher templates Excel."""

    def __init__(self, file_manager: IFileSystemManager):
        self._file_manager = file_manager

    def fill_and_save(
        self, template_path: Path, output_path: Path, data: List[DocumentGroup]
    ) -> None:
        if not template_path.exists():
            raise TemplateNotFoundError(
                f"Arquivo template não encontrado: {template_path}"
            )

        # 1. Copia o template para o local de saída
        self._file_manager.copy_file(template_path, output_path)

        # 2. Abre a cópia e a preenche
        try:
            workbook = openpyxl.load_workbook(output_path)
            sheet = workbook.active

            # Itera sobre cada grupo de documento (que representa um 'documento' lógico)
            for group in data:
                # O ManifestItem é o mesmo para todos os arquivos em um grupo
                manifest_info = group.files[0].associated_manifest_item
                if not manifest_info:
                    continue  # Pula se por algum motivo não houver info

                # Cria uma linha para cada arquivo físico no grupo
                for file in group.files:
                    row_data = [
                        manifest_info.revision,
                        manifest_info.title,
                        file.path.name,  # O nome do arquivo físico
                        # Lógica para extrair formato (ex: A1), se necessário
                        # Por enquanto, deixaremos em branco ou um valor padrão
                        manifest_info.metadata.get("FORMATO", ""),
                        manifest_info.metadata.get("DISCIPLINA", ""),
                        manifest_info.metadata.get("TIPO DE DOCUMENTO", ""),
                        manifest_info.metadata.get("PROPÓSITO", ""),
                        manifest_info.metadata.get("CAMINHO DATABOOK", ""),
                    ]
                    sheet.append(row_data)

            workbook.save(output_path)

        except Exception as e:
            raise TemplateFillError(f"Falha ao preencher o template {output_path}: {e}")
