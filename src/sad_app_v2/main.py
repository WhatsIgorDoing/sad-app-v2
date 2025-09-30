"""
Ponto de entrada principal da aplicação SAD App v2.0.
Configura a injeção de dependências e inicia a aplicação GUI.
"""

import customtkinter as ctk

from sad_app_v2.presentation.main_view import MainView
from sad_app_v2.presentation.view_controller import ViewController


def main():
    """Função principal que configura e inicia a aplicação."""
    from pathlib import Path

    from sad_app_v2.infrastructure.extraction import ProfiledExtractorService

    # Configurações do CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Configuração do serviço de extração completo
    config_path = Path("config/patterns.yaml")
    extractor_service = ProfiledExtractorService(config_path)

    # Criação da view principal
    app = MainView()

    # Criação e configuração do controller
    controller = ViewController(extractor_service)
    app.set_controller(controller)
    controller.set_view(app)

    # Carregar perfis no ComboBox
    profiles = ["PID", "GERAL"]  # Perfis além do RIR
    app.populate_profiles_dropdown(profiles)

    # Inicialização da aplicação
    app.mainloop()


if __name__ == "__main__":
    main()
