# main.py

"""
Ponto de entrada da aplicação SAD App v2.0.
"""

from src.sad_app_v2.presentation.controller import MainController
from src.sad_app_v2.presentation.main_view import MainView


def main():
    """
    Função principal da aplicação.
    """
    # Cria a view
    view = MainView()

    # Cria o controller e conecta com a view
    MainController(view)

    # Inicia a aplicação
    view.start()


if __name__ == "__main__":
    main()
