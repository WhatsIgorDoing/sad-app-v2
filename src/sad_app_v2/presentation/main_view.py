from typing import Dict, List

import customtkinter as ctk

from ..core.domain import DocumentFile


class MainView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("SAD App v2.0 - Sistema de Automação de Documentos")
        self.geometry("1280x720")
        self.minsize(960, 600)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.unrecognized_checkboxes: Dict[str, ctk.CTkCheckBox] = {}

        self._create_top_frame()
        self._create_tab_view()
        self._create_bottom_frame()

    def _create_top_frame(self):
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.manifest_entry = ctk.CTkEntry(
            self.top_frame, placeholder_text="Selecione o arquivo do manifesto..."
        )
        self.manifest_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.manifest_button = ctk.CTkButton(
            self.top_frame,
            text="Selecionar Manifesto...",
            command=lambda: self.controller and self.controller.select_manifest_file(),
        )
        self.manifest_button.grid(row=0, column=2, padx=10, pady=5)

        self.source_dir_entry = ctk.CTkEntry(
            self.top_frame, placeholder_text="Selecione a pasta com os documentos..."
        )
        self.source_dir_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.source_dir_button = ctk.CTkButton(
            self.top_frame,
            text="Selecionar Pasta...",
            command=lambda: self.controller
            and self.controller.select_source_directory(),
        )
        self.source_dir_button.grid(row=1, column=2, padx=10, pady=5)

        self.validate_button = ctk.CTkButton(
            self,
            text="VALIDAR LOTE",
            height=40,
            command=lambda: self.controller
            and self.controller.on_validate_batch_click(),
        )
        self.validate_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def _create_tab_view(self):
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.tab_validation = self.tab_view.add("Validação e Resolução")
        self._create_validation_tab_layout(self.tab_validation)

    def _create_validation_tab_layout(self, tab):
        tab.grid_columnconfigure((0, 1), weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Coluna Esquerda (Validados)
        self.validated_label = ctk.CTkLabel(tab, text="Arquivos Validados (0)")
        self.validated_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.validated_list = ctk.CTkTextbox(tab)
        self.validated_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Coluna Direita (Não Reconhecidos)
        self.unrecognized_label = ctk.CTkLabel(
            tab, text="Arquivos Não Reconhecidos (0)"
        )
        self.unrecognized_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.unrecognized_frame = ctk.CTkScrollableFrame(tab)
        self.unrecognized_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Painel de Resolução
        self.resolve_panel = ctk.CTkFrame(tab)
        self.resolve_panel.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.resolve_panel.grid_columnconfigure(0, weight=1)

        self.profile_combobox = ctk.CTkComboBox(self.resolve_panel, values=[])
        self.profile_combobox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.resolve_button = ctk.CTkButton(
            self.resolve_panel,
            text="Tentar Resolver Selecionados",
            command=lambda: self.controller and self.controller.on_resolve_click(),
        )
        self.resolve_button.grid(row=0, column=1, padx=10, pady=10)

        self.set_resolve_panel_state("disabled")

    def _create_bottom_frame(self):
        # ... (sem alterações aqui, mantenha o código anterior)
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.log_textbox = ctk.CTkTextbox(self.bottom_frame, height=100)
        self.log_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.log_textbox.configure(state="disabled")
        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

    # --- Métodos de Atualização da UI ---
    def set_resolve_panel_state(self, state: str):
        self.profile_combobox.configure(state=state)
        self.resolve_button.configure(state=state)

    def populate_profiles_dropdown(self, profiles: List[str]):
        self.profile_combobox.configure(values=profiles)
        if profiles:
            self.profile_combobox.set(profiles[0])

    def update_validated_list(self, validated_files: List[DocumentFile]):
        self.validated_label.configure(
            text=f"Arquivos Validados ({len(validated_files)})"
        )
        self.validated_list.configure(state="normal")
        self.validated_list.delete("1.0", ctk.END)
        if validated_files:
            self.validated_list.insert(
                "1.0", "\n".join(sorted([f.path.name for f in validated_files]))
            )
        self.validated_list.configure(state="disabled")

    def update_unrecognized_list(self, unrecognized_files: List[DocumentFile]):
        self.unrecognized_label.configure(
            text=f"Arquivos Não Reconhecidos ({len(unrecognized_files)})"
        )
        # Limpa o frame antigo
        for widget in self.unrecognized_frame.winfo_children():
            widget.destroy()
        self.unrecognized_checkboxes.clear()

        # Cria os novos checkboxes
        for i, file in enumerate(sorted(unrecognized_files, key=lambda f: f.path.name)):
            checkbox = ctk.CTkCheckBox(self.unrecognized_frame, text=file.path.name)
            checkbox.grid(row=i, column=0, padx=5, pady=2, sticky="w")
            self.unrecognized_checkboxes[file.path.name] = checkbox

    def start(self):
        self.mainloop()
