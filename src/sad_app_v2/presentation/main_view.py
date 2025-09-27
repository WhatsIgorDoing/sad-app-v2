import customtkinter as ctk

from .view_controller import ViewController


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = ViewController(self)  # Cria a instância do Controller

        # --- Configuração da Janela Principal ---
        self.title("SAD App v2.0 - Sistema de Automação de Documentos")
        self.geometry("1280x720")
        self.minsize(960, 600)

        # --- Layout Principal (Grid) ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Widgets ---
        self._create_top_frame()
        self._create_tab_view()
        self._create_bottom_frame()

    def _create_top_frame(self):
        """Cria o frame superior para seleção de arquivos e o botão de validação."""
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.manifest_label = ctk.CTkLabel(self.top_frame, text="Manifesto de Entrada:")
        self.manifest_label.grid(row=0, column=0, padx=10, pady=5)
        self.manifest_entry = ctk.CTkEntry(
            self.top_frame, placeholder_text="Selecione o arquivo do manifesto..."
        )
        self.manifest_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        # Conecta o botão ao método do controller
        self.manifest_button = ctk.CTkButton(
            self.top_frame,
            text="Selecionar...",
            command=self.controller.select_manifest_file,
        )
        self.manifest_button.grid(row=0, column=2, padx=10, pady=5)

        self.source_dir_label = ctk.CTkLabel(self.top_frame, text="Pasta de Origem:")
        self.source_dir_label.grid(row=1, column=0, padx=10, pady=5)
        self.source_dir_entry = ctk.CTkEntry(
            self.top_frame, placeholder_text="Selecione a pasta com os documentos..."
        )
        self.source_dir_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        # Conecta o botão ao método do controller
        self.source_dir_button = ctk.CTkButton(
            self.top_frame,
            text="Selecionar...",
            command=self.controller.select_source_directory,
        )
        self.source_dir_button.grid(row=1, column=2, padx=10, pady=5)

        # Conecta o botão ao método do controller
        self.validate_button = ctk.CTkButton(
            self,
            text="VALIDAR LOTE",
            height=40,
            command=self.controller.on_validate_batch_click,
        )
        self.validate_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def _create_tab_view(self):
        """Cria a visão de abas principal."""
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.tab_validation = self.tab_view.add("Validação e Resolução")
        self._create_validation_tab_layout(self.tab_validation)

    def _create_validation_tab_layout(self, tab):
        """Cria o layout da aba de validação com duas colunas."""
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        # Coluna Esquerda
        self.validated_label = ctk.CTkLabel(tab, text="Arquivos Validados (0)")
        self.validated_label.grid(row=0, column=0, padx=10, pady=5)
        self.validated_list = ctk.CTkTextbox(tab)
        self.validated_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.validated_list.configure(state="disabled")

        # Coluna Direita
        self.unrecognized_label = ctk.CTkLabel(
            tab, text="Arquivos Não Reconhecidos (0)"
        )
        self.unrecognized_label.grid(row=0, column=1, padx=10, pady=5)
        self.unrecognized_list = ctk.CTkTextbox(tab)
        self.unrecognized_list.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.unrecognized_list.configure(state="disabled")

        self.update_results_lists([], [])  # Limpa as listas inicialmente

    def _create_bottom_frame(self):
        """Cria o frame inferior para o log e a barra de progresso."""
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.log_textbox = ctk.CTkTextbox(self.bottom_frame, height=100)
        self.log_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.log_textbox.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(self.bottom_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)

    def update_results_lists(self, validated_files, unrecognized_files):
        """Limpa e preenche as caixas de texto com os resultados."""
        self.validated_label.configure(
            text=f"Arquivos Validados ({len(validated_files)})"
        )
        self.validated_list.configure(state="normal")
        self.validated_list.delete("1.0", ctk.END)
        self.validated_list.insert(
            "1.0", "\n".join(f.path.name for f in validated_files)
        )
        self.validated_list.configure(state="disabled")

        self.unrecognized_label.configure(
            text=f"Arquivos Não Reconhecidos ({len(unrecognized_files)})"
        )
        self.unrecognized_list.configure(state="normal")
        self.unrecognized_list.delete("1.0", ctk.END)
        self.unrecognized_list.insert(
            "1.0", "\n".join(f.path.name for f in unrecognized_files)
        )
        self.unrecognized_list.configure(state="disabled")

    def start(self):
        """Inicia o loop principal da aplicação."""
        self.mainloop()
