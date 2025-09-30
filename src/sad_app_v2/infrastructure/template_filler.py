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


def _get_filename_with_revision(original_filename: str, revision: str) -> str:
    """
    Constrói o nome do arquivo com a revisão adicionada antes da extensão.

    Exemplo:
    - "arquivo.pdf" + "A" -> "arquivo_A.pdf"
    - "arquivo" + "B" -> "arquivo_B"
    """
    name_parts = original_filename.rsplit(".", 1)
    if len(name_parts) == 2:
        base_name, extension = name_parts
        return f"{base_name}_{revision}.{extension}"
    else:
        # Arquivo sem extensão
        return f"{original_filename}_{revision}"


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

            # Encontrar onde inserir os dados (após cabeçalho, antes de "FIM")
            insert_row = 2  # Por padrão, inserir na linha 2 (após cabeçalho)

            # Procurar pela linha "FIM" para inserir antes dela
            for row_num in range(2, sheet.max_row + 1):
                cell_value = sheet.cell(row=row_num, column=1).value
                if cell_value and str(cell_value).upper() == "FIM":
                    insert_row = row_num
                    break

            # Preparar todos os dados primeiro
            all_rows_data = []
            for group in data:
                # O ManifestItem é o mesmo para todos os arquivos em um grupo
                manifest_info = group.files[0].associated_manifest_item
                if not manifest_info:
                    continue  # Pula se por algum motivo não houver info

                # Cria uma linha para cada arquivo físico no grupo
                for file in group.files:
                    # Construir nome do arquivo com revisão (como ele ficará após ser movido)
                    revision = manifest_info.revision
                    filename_with_revision = _get_filename_with_revision(
                        file.path.name, revision
                    )

                    # Ordem correta dos campos conforme template:
                    row_data = [
                        manifest_info.document_code,  # DOCUMENTO
                        manifest_info.revision,  # REVISÃO
                        manifest_info.title,  # TÍTULO
                        filename_with_revision,  # ARQUIVO (nome final com revisão)
                        manifest_info.metadata.get("FORMATO", "A4"),  # FORMATO
                        manifest_info.metadata.get("DISCIPLINA", ""),  # DISCIPLINA
                        manifest_info.metadata.get(
                            "TIPO DE DOCUMENTO", ""
                        ),  # TIPO DE DOCUMENTO
                        manifest_info.metadata.get("PROPÓSITO", ""),  # PROPÓSITO
                        manifest_info.metadata.get(
                            "CAMINHO DATABOOK", ""
                        ),  # CAMINHO DATABOOK
                    ]
                    all_rows_data.append(row_data)

            # Inserir todas as linhas necessárias ANTES da linha "FIM"
            if all_rows_data:
                # Inserir todas as linhas necessárias antes da linha "FIM"
                for i in range(len(all_rows_data)):
                    sheet.insert_rows(insert_row)

                # Agora preencher os dados (FIM foi empurrada para baixo)
                for i, row_data in enumerate(all_rows_data):
                    target_row = insert_row + i
                    # Preencher a linha com os dados
                    for col_num, value in enumerate(row_data, 1):
                        sheet.cell(row=target_row, column=col_num, value=value)

            workbook.save(output_path)

        except Exception as e:
            raise TemplateFillError(f"Falha ao preencher o template {output_path}: {e}")
