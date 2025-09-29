# src/sad_app_v2/presentation/view_controller.py

import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
import threading
import yaml
from typing import TYPE_CHECKING, List

from ..core.domain import DocumentFile
from ..core.use_cases.validate_batch import ValidateBatchUseCase
from ..core.use_cases.resolve_exception import ResolveUnrecognizedFileUseCase
from ..infrastructure.excel_reader import ExcelManifestRepository
from ..infrastructure.file_system import FileSystemFileRepository
from ..infrastructure.extraction import ProfiledExtractorService
from ..core.interfaces import CoreError

if TYPE_CHECKING:
    from .main_view import MainView


class ViewController:
    def __init__(self, view: "MainView"):
        self.view = view
        # Estado da Aplicação
        self.manifest_path: Path | None = None
        self.source_directory: Path | None = None
        self.validated_files: List[DocumentFile] = []
        self.unrecognized_files: List[DocumentFile] = []
        self.all_manifest_items = []

        # Carrega os perfis na inicialização
        self.extractor_service = ProfiledExtractorService(Path("config/patterns.yaml"))
        self.view.populate_profiles_dropdown(
            list(self.extractor_service._profiles.keys())
        )

    def select_manifest_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecione o Manifesto", filetypes=[("Arquivos Excel", "*.xlsx")]
        )
        if file_path:
            self.manifest_path = Path(file_path)
            self.view.manifest_entry.delete(0, ctk.END)
            self.view.manifest_entry.insert(0, str(self.manifest_path))

    def select_source_directory(self):
        dir_path = filedialog.askdirectory(title="Selecione a Pasta de Origem")
        if dir_path:
            self.source_directory = Path(dir_path)
            self.view.source_dir_entry.delete(0, ctk.END)
            self.view.source_dir_entry.insert(0, str(self.source_directory))

    def on_validate_batch_click(self):
        if not self.manifest_path or not self.source_directory:
            messagebox.showerror(
                "Erro", "Por favor, selecione o manifesto e o diretório."
            )
            return

        self.view.validate_button.configure(state="disabled", text="Validando...")
        self._update_ui_lists()
        threading.Thread(target=self._run_validation, daemon=True).start()

    def _run_validation(self):
        try:
            manifest_repo = ExcelManifestRepository()
            file_repo = FileSystemFileRepository()
            use_case = ValidateBatchUseCase(manifest_repo, file_repo)

            # Guarda os itens do manifesto para uso na resolução
            self.all_manifest_items = manifest_repo.load_from_file(self.manifest_path)

            # Executa a validação
            self.validated_files, self.unrecognized_files = use_case.execute(
                self.manifest_path, self.source_directory
            )

            # Atualiza a UI na thread principal
            self.view.after(0, self._update_ui_lists)

        except CoreError as e:
            self.view.after(0, messagebox.showerror, "Erro de Validação", str(e))
        finally:
            self.view.after(
                0,
                self.view.validate_button.configure,
                {"state": "normal", "text": "VALIDAR LOTE"},
            )

    def on_resolve_click(self):
        selected_filenames = [
            name
            for name, checkbox in self.view.unrecognized_checkboxes.items()
            if checkbox.get() == 1
        ]
        profile_id = self.view.profile_combobox.get()

        if not selected_filenames:
            messagebox.showinfo(
                "Nenhuma Seleção",
                "Por favor, selecione um ou mais arquivos para resolver.",
            )
            return

        self.view.set_resolve_panel_state("disabled")

        files_to_resolve = [
            f for f in self.unrecognized_files if f.path.name in selected_filenames
        ]

        for file in files_to_resolve:
            threading.Thread(
                target=self._run_resolution, args=(file, profile_id), daemon=True
            ).start()

    def _run_resolution(self, file_to_resolve: DocumentFile, profile_id: str):
        try:
            use_case = ResolveUnrecognizedFileUseCase(
                self.extractor_service, self.extractor_service
            )
            resolved_file = use_case.execute(
                file_to_resolve, profile_id, self.all_manifest_items
            )

            # Atualiza as listas de estado
            self.unrecognized_files.remove(file_to_resolve)
            self.validated_files.append(resolved_file)

            # Agenda a atualização da UI
            self.view.after(0, self._update_ui_lists)

        except CoreError as e:
            self.view.after(
                0,
                messagebox.showinfo,
                "Falha na Resolução",
                f"Erro ao resolver '{file_to_resolve.path.name}':\n\n{e}",
            )
        finally:
            self.view.after(0, self.view.set_resolve_panel_state, "normal")

    def _update_ui_lists(self):
        """Método central para atualizar as listas da UI com o estado atual."""
        self.view.update_validated_list(self.validated_files)
        self.view.update_unrecognized_list(self.unrecognized_files)

        if self.unrecognized_files:
            self.view.set_resolve_panel_state("normal")
        else:
            self.view.set_resolve_panel_state("disabled")
