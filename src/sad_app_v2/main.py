"""
Ponto de entrada principal da aplicação SAD App v2.0.
Configura a injeção de dependências e inicia a aplicação GUI.
"""

import customtkinter as ctk

from sad_app_v2.presentation.main_view import MainView
from sad_app_v2.presentation.view_controller import ViewController


def main():
    """Função principal que configura e inicia a aplicação."""
    # Configurações do CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Implementação simples do extractor service
    class SimpleExtractorService:
        def extract_text(self, file, profile_id):
            return file.path.stem

        def find_code(self, text, profile_id):
            # Implementação simples: retorna o próprio texto como código
            return text if text else None

    extractor_service = SimpleExtractorService()

    # Criação da view principal
    app = MainView()

    # Criação e configuração do controller
    controller = ViewController(extractor_service)
    app.set_controller(controller)
    controller.set_view(app)

    # Inicialização da aplicação
    app.mainloop()


if __name__ == "__main__":
    main()
