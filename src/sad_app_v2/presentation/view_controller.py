# src/sad_app_v2/presentation/view_controller.py

import threading
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

import customtkinter as ctk

# --- Importações da nossa arquitetura ---
from ..core.interfaces import CoreError
from ..core.use_cases.validate_batch import ValidateBatchUseCase
from ..infrastructure.excel_reader import ExcelManifestRepository
from ..infrastructure.file_system import FileSystemFileRepository

if TYPE_CHECKING:
    from .main_view import MainView


class ViewController:
    def __init__(self, view: "MainView"):
        self.view = view
        self.manifest_path: Path | None = None
        self.source_directory: Path | None = None

    def select_manifest_file(self):
        """Abre um diálogo para selecionar o arquivo de manifesto."""
        file_path = filedialog.askopenfilename(
            title="Selecione o Manifesto Excel",
            filetypes=[("Arquivos Excel", "*.xlsx")],
        )
        if file_path:
            self.manifest_path = Path(file_path)
            self.view.manifest_entry.delete(0, ctk.END)
            self.view.manifest_entry.insert(0, str(self.manifest_path))

    def select_source_directory(self):
        """Abre um diálogo para selecionar o diretório de origem."""
        dir_path = filedialog.askdirectory(title="Selecione a Pasta de Origem")
        if dir_path:
            self.source_directory = Path(dir_path)
            self.view.source_dir_entry.delete(0, ctk.END)
            self.view.source_dir_entry.insert(0, str(self.source_directory))

    def on_validate_batch_click(self):
        """Inicia a validação em uma thread separada para não congelar a UI."""
        if not self.manifest_path or not self.source_directory:
            messagebox.showerror(
                "Erro de Entrada",
                "Por favor, selecione o arquivo de manifesto e a pasta de origem.",
            )
            return

        # Desabilitar o botão para evitar cliques duplos
        self.view.validate_button.configure(state="disabled", text="Validando...")
        self.view.update_results_lists([], [])  # Limpa os resultados anteriores

        # A execução da lógica de negócio pesada ocorre em outra thread
        thread = threading.Thread(
            target=self._run_validation,
            args=(self.manifest_path, self.source_directory),
        )
        thread.start()

    def _run_validation(self, manifest_path: Path, source_dir: Path):
        """
        Método que executa o caso de uso e atualiza a UI.
        Este método roda na thread de trabalho.
        """
        try:
            # 1. Composição: Montamos nossas dependências aqui
            manifest_repo = ExcelManifestRepository()
            file_repo = FileSystemFileRepository()
            use_case = ValidateBatchUseCase(manifest_repo, file_repo)

            # 2. Execução: Chamamos o caso de uso
            validated, unrecognized = use_case.execute(manifest_path, source_dir)

            # 3. Atualização da UI: Passamos a tarefa de volta para a thread principal
            self.view.after(0, self.view.update_results_lists, validated, unrecognized)

        except CoreError as e:
            # 4. Tratamento de Erros
            self.view.after(0, messagebox.showerror, "Erro na Validação", str(e))
        finally:
            # 5. Reabilitar o botão, não importa o que aconteça
            self.view.after(
                0,
                self.view.validate_button.configure,
                {"state": "normal", "text": "VALIDAR LOTE"},
            )
