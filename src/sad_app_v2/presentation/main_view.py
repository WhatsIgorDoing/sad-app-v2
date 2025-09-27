import customtkinter as ctk


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Configuração da Janela Principal ---
        self.title("SAD App v2.0 - Sistema de Automação de Documentos")
        self.geometry("1280x720")
        self.minsize(960, 600)

        # --- Layout Principal (Grid) ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # A área das abas se expandirá

        # --- Widgets ---
        self._create_top_frame()
        self._create_tab_view()
        self._create_bottom_frame()

    def _create_top_frame(self):
        """Cria o frame superior para seleção de arquivos e o botão de validação."""
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        # Manifesto
        self.manifest_label = ctk.CTkLabel(self.top_frame, text="Manifesto de Entrada:")
        self.manifest_label.grid(row=0, column=0, padx=10, pady=5)
        self.manifest_entry = ctk.CTkEntry(
            self.top_frame, placeholder_text="Selecione o arquivo do manifesto..."
        )
        self.manifest_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.manifest_button = ctk.CTkButton(self.top_frame, text="Selecionar...")
        self.manifest_button.grid(row=0, column=2, padx=10, pady=5)

        # Pasta de Origem
        self.source_dir_label = ctk.CTkLabel(self.top_frame, text="Pasta de Origem:")
        self.source_dir_label.grid(row=1, column=0, padx=10, pady=5)
        self.source_dir_entry = ctk.CTkEntry(
            self.top_frame, placeholder_text="Selecione a pasta com os documentos..."
        )
        self.source_dir_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.source_dir_button = ctk.CTkButton(self.top_frame, text="Selecionar...")
        self.source_dir_button.grid(row=1, column=2, padx=10, pady=5)

        # Botão de Validação
        self.validate_button = ctk.CTkButton(self, text="VALIDAR LOTE", height=40)
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

    def start(self):
        """Inicia o loop principal da aplicação."""
        self.mainloop()
