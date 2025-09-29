# src/sad_app_v2/presentation/view_controller.py

import threading
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List

import customtkinter as ctk

from sad_app_v2.core.exceptions import CoreError
from sad_app_v2.core.use_cases.organize_lots import OrganizeAndGenerateLotsUseCase
from sad_app_v2.core.use_cases.resolve_exception import ResolveUnrecognizedFileUseCase
from sad_app_v2.core.use_cases.validate_batch import ValidateBatchUseCase
from sad_app_v2.infrastructure.file_system import (
    FileSystemFileRepository,
    SafeFileSystemManager,
)
from sad_app_v2.infrastructure.services import GreedyLotBalancerService
from sad_app_v2.infrastructure.template_filler import OpenpyxlTemplateFiller

from ..core.domain import DocumentFile
from ..infrastructure.excel_reader import ExcelManifestRepository


class ViewController:
    def __init__(self, extractor_service):
        self.extractor_service = extractor_service
        self.view = None
        # Estado da Aplicação
        self.manifest_path: Path | None = None
        self.source_directory: Path | None = None
        self.output_directory: Path | None = None
        self.master_template_path: Path | None = None

        self.validated_files: List[DocumentFile] = []
        self.unrecognized_files: List[DocumentFile] = []
        self.all_manifest_items = []

    def set_view(self, view):
        """Define a view associada ao controller."""
        self.view = view

    # --- Métodos de Seleção de Arquivos/Pastas ---
    def select_manifest_file(self):
        path = filedialog.askopenfilename(
            title="Selecione o Manifesto", filetypes=[("Excel", "*.xlsx")]
        )
        if path:
            self.manifest_path = Path(path)
            self.view.manifest_entry.delete(0, ctk.END)
            self.view.manifest_entry.insert(0, str(path))

    def select_source_directory(self):
        path = filedialog.askdirectory(title="Selecione a Pasta de Origem")
        if path:
            self.source_directory = Path(path)
            self.view.source_dir_entry.delete(0, ctk.END)
            self.view.source_dir_entry.insert(0, str(path))

    def select_output_directory(self):
        path = filedialog.askdirectory(title="Selecione a Pasta de Destino Raiz")
        if path:
            self.output_directory = Path(path)
            self.view.output_dir_entry.delete(0, ctk.END)
            self.view.output_dir_entry.insert(0, str(path))

    def select_master_template_file(self):
        path = filedialog.askopenfilename(
            title="Selecione o Template de Manifesto", filetypes=[("Excel", "*.xlsx")]
        )
        if path:
            self.master_template_path = Path(path)
            self.view.template_entry.delete(0, ctk.END)
            self.view.template_entry.insert(0, str(path))

    # --- Lógica dos Casos de Uso ---
    def on_validate_batch_click(self):
        if not self.manifest_path or not self.source_directory:
            messagebox.showerror(
                "Erro", "Por favor, selecione o manifesto e o diretório de origem."
            )
            return

        self._set_ui_busy(True, "Validando...")
        self.view.clear_log()
        self.view.add_log_message("Iniciando validação...")
        threading.Thread(target=self._run_validation, daemon=True).start()

    def _run_validation(self):
        try:
            # ... (código existente)
            manifest_repo = ExcelManifestRepository()
            file_repo = FileSystemFileRepository()
            use_case = ValidateBatchUseCase(manifest_repo, file_repo)
            self.all_manifest_items = manifest_repo.load_from_file(self.manifest_path)
            self.validated_files, self.unrecognized_files = use_case.execute(
                self.manifest_path, self.source_directory
            )

            self.view.after(
                0,
                self.view.add_log_message,
                f"Validação concluída: {len(self.validated_files)} válidos, "
                f"{len(self.unrecognized_files)} não reconhecidos.",
            )
            self.view.after(0, self._update_ui_lists)

        except CoreError as e:
            self.view.after(0, messagebox.showerror, "Erro de Validação", str(e))
        finally:
            self.view.after(0, self._set_ui_busy, False, "VALIDAR LOTE")

    def on_resolve_click(self):
        # ... (código existente)
        selected_filenames = [
            name
            for name, cb in self.view.unrecognized_checkboxes.items()
            if cb.get() == 1
        ]
        if not selected_filenames:
            messagebox.showinfo("Seleção", "Selecione arquivos para resolver.")
            return

        self.view.set_resolve_panel_state("disabled")
        profile_id = self.view.profile_combobox.get()
        files_to_resolve = [
            f for f in self.unrecognized_files if f.path.name in selected_filenames
        ]

        for file in files_to_resolve:
            threading.Thread(
                target=self._run_resolution, args=(file, profile_id), daemon=True
            ).start()

    def _run_resolution(self, file: DocumentFile, profile_id: str):
        try:
            use_case = ResolveUnrecognizedFileUseCase(
                self.extractor_service, self.extractor_service
            )
            resolved_file = use_case.execute(file, profile_id, self.all_manifest_items)
            self.unrecognized_files.remove(file)
            self.validated_files.append(resolved_file)
            self.view.after(
                0,
                self.view.add_log_message,
                f"Arquivo '{file.path.name}' resolvido com sucesso.",
            )
            self.view.after(0, self._update_ui_lists)
        except CoreError as e:
            self.view.after(
                0,
                messagebox.showinfo,
                "Falha",
                f"Erro ao resolver '{file.path.name}':\n{e}",
            )
        finally:
            self.view.after(0, self.view.set_resolve_panel_state, "normal")

    def on_organize_lots_click(self):
        # 1. Validar entradas da UI
        try:
            max_docs = int(self.view.max_docs_entry.get())
            start_seq = int(self.view.seq_num_entry.get())
            pattern = self.view.lot_pattern_entry.get()
            if not all([self.output_directory, self.master_template_path, pattern]):
                raise ValueError("Campos obrigatórios não preenchidos.")
        except (ValueError, TypeError):
            messagebox.showerror(
                "Erro de Configuração",
                "Verifique as configurações de saída. Campos numéricos "
                "devem ser números e todos os caminhos devem ser selecionados.",
            )
            return

        self._set_ui_busy(True, "Organizando...")
        self.view.clear_log()
        self.view.add_log_message("Iniciando organização final...")

        config = {
            "validated_files": self.validated_files,
            "output_directory": self.output_directory,
            "master_template_path": self.master_template_path,
            "max_docs_per_lot": max_docs,
            "start_sequence_number": start_seq,
            "lot_name_pattern": pattern,
        }
        threading.Thread(
            target=self._run_organization, kwargs=config, daemon=True
        ).start()

    def _run_organization(self, **kwargs):
        try:
            # Composição final dos serviços
            balancer = GreedyLotBalancerService()
            file_manager = SafeFileSystemManager()
            template_filler = OpenpyxlTemplateFiller(file_manager)
            use_case = OrganizeAndGenerateLotsUseCase(
                balancer, file_manager, template_filler
            )

            # Execução
            result = use_case.execute(**kwargs)

            if result.success:
                msg = (
                    f"Organização concluída!\n\n- {result.lots_created} lotes "
                    f"criados.\n- {result.files_moved} arquivos movidos."
                )
                self.view.after(
                    0, self.view.add_log_message, "SUCESSO: " + msg.replace("\n\n", " ")
                )
                self.view.after(0, messagebox.showinfo, "Sucesso", msg)
            else:
                raise CoreError(result.message)

        except CoreError as e:
            self.view.after(0, self.view.add_log_message, f"ERRO: {e}")
            self.view.after(0, messagebox.showerror, "Erro na Organização", str(e))
        finally:
            self.view.after(0, self._set_ui_busy, False, "VALIDAR LOTE")
            self.view.after(0, self._reset_state)

    def _update_ui_lists(self):
        """Método central para atualizar as listas da UI com o estado atual."""
        self.view.update_validated_list(self.validated_files)
        self.view.update_unrecognized_list(self.unrecognized_files)

    def _set_ui_busy(self, busy: bool, status_text: str = ""):
        """Controla o estado ocupado da UI."""
        self.view.set_organize_button_state("disabled" if busy else "normal")
        if status_text:
            self.view.add_log_message(f"STATUS: {status_text}")

    def _reset_state(self):
        """Reinicia o estado após operações."""
        self.view.progress_bar.set(0)
        self.view.add_log_message("Pronto para nova operação.")

        if self.unrecognized_files:
            self.view.set_resolve_panel_state("normal")
        else:
            self.view.set_resolve_panel_state("disabled")
