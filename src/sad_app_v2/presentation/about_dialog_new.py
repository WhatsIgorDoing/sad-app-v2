import customtkinter as ctk


class AboutDialog(ctk.CTkToplevel):
    """Janela de diálogo 'Sobre' que exibe informações sobre a aplicação."""

    def __init__(self, parent):
        super().__init__(parent)

        # Configuração da janela
        self.title("Sobre o SAD App v2.0")
        self.geometry("500x400")
        self.resizable(False, False)
        self.transient(parent)  # Torna a janela dependente da janela principal
        self.grab_set()  # Torna a janela modal

        # Centraliza a janela em relação à janela pai
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        # Cria o layout
        self._create_widgets()

    def _create_widgets(self):
        """Cria os widgets da janela de diálogo."""

        self.grid_columnconfigure(0, weight=1)

        # Título
        title_label = ctk.CTkLabel(
            self, text="SAD App v2.0", font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        subtitle_label = ctk.CTkLabel(
            self, text="Sistema de Automação de Documentos", font=ctk.CTkFont(size=16)
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Conteúdo
        content_frame = ctk.CTkFrame(self)
        content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)

        info_text = (
            "Desenvolvido por: Igor Bueno\n"
            "Copyright © 2025 Igor Bueno\n"
            "Todos os direitos reservados.\n\n"
            "Esta ferramenta automatiza o processo de validação, organização\n"
            "e geração de lotes de documentos, facilitando a gestão de grandes\n"
            "volumes de arquivos de acordo com regras de negócio específicas.\n\n"
            "Data de criação: Setembro/2025\n"
            "Versão: 2.0.0"
        )

        info_label = ctk.CTkLabel(
            content_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left",
            anchor="w",
            wraplength=450,  # Quebra de linha para textos longos
        )
        info_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsw")

        # Botão Fechar
        close_button = ctk.CTkButton(
            self, text="Fechar", command=self.destroy, width=100
        )
        close_button.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="e")
