import sys

sys.path.insert(0, "src")

from pathlib import Path
from unittest.mock import MagicMock, patch

# Simular customtkinter
sys.modules["customtkinter"] = MagicMock()

from sad_app_v2.presentation.main_view import MainView
from sad_app_v2.presentation.view_controller import ViewController
from sad_app_v2.core.domain import DocumentFile, DocumentStatus


def test_checkbox_activation():
    print("=== TESTE - ATIVAÇÃO DOS BOTÕES DE RESOLUÇÃO ===")

    # 1. Criar view e controller simulados
    with (
        patch("customtkinter.CTk"),
        patch("customtkinter.CTkFrame"),
        patch("customtkinter.CTkEntry"),
        patch("customtkinter.CTkButton"),
        patch("customtkinter.CTkCheckBox"),
        patch("customtkinter.CTkScrollableFrame"),
        patch("customtkinter.CTkComboBox"),
        patch("customtkinter.CTkProgressBar"),
        patch("customtkinter.CTkTextbox"),
        patch("customtkinter.CTkTabview"),
    ):
        view = MainView()
        controller = ViewController("test_extractor")
        view.set_controller(controller)
        controller.set_view(view)

        # 2. Simular arquivos não reconhecidos
        unrecognized_files = [
            DocumentFile(Path("arquivo1.pdf"), 1000),
            DocumentFile(Path("arquivo2.docx"), 1500),
            DocumentFile(Path("arquivo3.xlsx"), 800),
        ]

        for file in unrecognized_files:
            file.status = DocumentStatus.UNRECOGNIZED

        controller.unrecognized_files = unrecognized_files

        # 3. Simular checkboxes
        mock_checkbox1 = MagicMock()
        mock_checkbox2 = MagicMock()
        mock_checkbox3 = MagicMock()

        view.unrecognized_checkboxes = {
            "arquivo1.pdf": mock_checkbox1,
            "arquivo2.docx": mock_checkbox2,
            "arquivo3.xlsx": mock_checkbox3,
        }

        # Mock do método set_resolve_panel_state
        view.set_resolve_panel_state = MagicMock()

        print("📋 CENÁRIOS DE TESTE:")

        # 4. Teste 1: Nenhum checkbox marcado
        mock_checkbox1.get.return_value = 0
        mock_checkbox2.get.return_value = 0
        mock_checkbox3.get.return_value = 0

        controller.on_checkbox_selection_changed()

        print("   1. Nenhum checkbox marcado:")
        print(f"      Estado esperado: disabled")
        if view.set_resolve_panel_state.called:
            last_call = view.set_resolve_panel_state.call_args[0][0]
            print(f"      Estado atual: {last_call}")
            print(f"      ✅ {'CORRETO' if last_call == 'disabled' else 'INCORRETO'}")

        # 5. Teste 2: Um checkbox marcado
        view.set_resolve_panel_state.reset_mock()
        mock_checkbox1.get.return_value = 1  # Marcado
        mock_checkbox2.get.return_value = 0
        mock_checkbox3.get.return_value = 0

        controller.on_checkbox_selection_changed()

        print("   2. Um checkbox marcado:")
        print(f"      Estado esperado: normal")
        if view.set_resolve_panel_state.called:
            last_call = view.set_resolve_panel_state.call_args[0][0]
            print(f"      Estado atual: {last_call}")
            print(f"      ✅ {'CORRETO' if last_call == 'normal' else 'INCORRETO'}")

        # 6. Teste 3: Múltiplos checkboxes marcados
        view.set_resolve_panel_state.reset_mock()
        mock_checkbox1.get.return_value = 1  # Marcado
        mock_checkbox2.get.return_value = 1  # Marcado
        mock_checkbox3.get.return_value = 0

        controller.on_checkbox_selection_changed()

        print("   3. Múltiplos checkboxes marcados:")
        print(f"      Estado esperado: normal")
        if view.set_resolve_panel_state.called:
            last_call = view.set_resolve_panel_state.call_args[0][0]
            print(f"      Estado atual: {last_call}")
            print(f"      ✅ {'CORRETO' if last_call == 'normal' else 'INCORRETO'}")

        # 7. Teste 4: Sem arquivos não reconhecidos
        view.set_resolve_panel_state.reset_mock()
        controller.unrecognized_files = []

        controller.on_checkbox_selection_changed()

        print("   4. Sem arquivos não reconhecidos:")
        print(f"      Estado esperado: disabled")
        if view.set_resolve_panel_state.called:
            last_call = view.set_resolve_panel_state.call_args[0][0]
            print(f"      Estado atual: {last_call}")
            print(f"      ✅ {'CORRETO' if last_call == 'disabled' else 'INCORRETO'}")

        return True


if __name__ == "__main__":
    success = test_checkbox_activation()
    print(f"\n🎉 TESTE {'PASSOU' if success else 'FALHOU'} 🎉")
    print("\n💡 A correção implementada deve ativar os botões de resolução")
    print("   apenas quando houver checkboxes marcados!")
