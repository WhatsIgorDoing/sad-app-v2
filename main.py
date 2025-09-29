from src.sad_app_v2.presentation.main_view import MainView
from src.sad_app_v2.presentation.view_controller import ViewController


def main():
    """
    Função principal da aplicação.
    """
    # Cria a view primeiro
    app = MainView(None)

    # Cria o controller e o atribui à view
    controller = ViewController(app)
    app.controller = controller

    # Inicia a aplicação
    app.start()


if __name__ == "__main__":
    main()
