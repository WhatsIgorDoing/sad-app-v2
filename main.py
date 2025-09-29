from src.sad_app_v2.presentation.main_view import MainView


def main():
    """
    Função principal da aplicação.
    """
    # Cria a view (que já cria o controller internamente)
    app = MainView()

    # Inicia a aplicação
    app.start()


if __name__ == "__main__":
    main()
