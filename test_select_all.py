"""
Script para testar a funcionalidade de "Selecionar Todos"
em arquivos não reconhecidos.
"""
import sys
from pathlib import Path

# Adicionar o diretório principal ao caminho de importação
sys.path.insert(0, str(Path(__file__).parent))

import customtkinter as ctk

from src.sad_app_v2.core.domain import DocumentFile, DocumentStatus
from src.sad_app_v2.presentation.main_view import MainView
from src.sad_app_v2.presentation.view_controller import ViewController


class MockExtractor:
    def extract_text(self, file, profile):
        return "Texto extraído de teste"


def main():
    # Configurar o ambiente de teste
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Criar view e controller
    view = MainView()
    controller = ViewController(MockExtractor())
    view.set_controller(controller)
    controller.set_view(view)

    # Simular alguns arquivos não reconhecidos
    unrecognized_files = [
        DocumentFile(
            Path(f"arquivo_teste_{i}.pdf"), 1000, status=DocumentStatus.UNRECOGNIZED
        )
        for i in range(1, 11)
    ]

    # Atualizar a lista
    view.update_unrecognized_list(unrecognized_files)
    controller.unrecognized_files = unrecognized_files

    # Habilitar painel de resolução
    view.set_resolve_panel_state("normal")

    # Adicionar mensagem de log
    view.add_log_message("Teste de seleção em lote:")
    view.add_log_message(
        "1. Clique em 'Selecionar Todos' para marcar todos os arquivos"
    )
    view.add_log_message("2. Clique novamente para desmarcar todos")
    view.add_log_message("3. Teste o botão 'Tentar Resolver Selecionados'")

    # Iniciar a interface
    view.start()


if __name__ == "__main__":
    main()
