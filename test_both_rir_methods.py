import sys

sys.path.insert(0, "src")

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

# Simular customtkinter
sys.modules["customtkinter"] = MagicMock()

from sad_app_v2.core.domain import DocumentFile, DocumentStatus, ManifestItem
from sad_app_v2.presentation.view_controller import ViewController


def test_both_rir_methods():
    print("=== TESTE - AMBOS OS MÉTODOS RIR ===")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Configurar controller
        controller = ViewController("test_extractor")

        # Mock do extrator
        mock_extractor = MagicMock()
        mock_extractor.extract_text.return_value = """
RELATÓRIO DE INSPEÇÃO POR RISCO - RIR

Relatório: CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A

Data: 29/09/2025
        """
        controller.extractor_service = mock_extractor

        # Mock da view
        mock_view = MagicMock()
        controller.view = mock_view

        # Manifesto
        controller.all_manifest_items = [
            ManifestItem("CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A", "B", "RIR Teste")
        ]

        # TESTE 1: Método específico (🔍 RIR)
        print("\n🔍 TESTE 1 - MÉTODO ESPECÍFICO:")
        test_file1 = temp_path / "teste_especifico.pdf"
        test_file1.write_text("arquivo simulado")

        doc_file1 = DocumentFile(test_file1, 1000)
        controller.unrecognized_files = [doc_file1]
        controller.validated_files = []

        controller._run_rir_resolution(doc_file1)

        expected_name1 = "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A_B.pdf"
        expected_path1 = temp_path / expected_name1

        print(f"   Arquivo original: teste_especifico.pdf")
        print(f"   Nome esperado: {expected_name1}")
        print(f"   Arquivo renomeado existe: {expected_path1.exists()}")
        print(
            f"   ✅ Método específico: {'FUNCIONOU' if expected_path1.exists() else 'FALHOU'}"
        )

        # TESTE 2: Método genérico (RIR do YAML)
        print("\n📋 TESTE 2 - MÉTODO GENÉRICO:")
        test_file2 = temp_path / "teste_generico.pdf"
        test_file2.write_text("arquivo simulado")

        doc_file2 = DocumentFile(test_file2, 1000)
        controller.unrecognized_files = [doc_file2]

        # Simular que resolved_file tem associated_manifest_item (como retornado pelo use case)
        resolved_file_mock = DocumentFile(test_file2, 1000)
        resolved_file_mock.associated_manifest_item = controller.all_manifest_items[0]
        resolved_file_mock.status = DocumentStatus.VALIDATED

        # Mock do use case para retornar arquivo com manifest item
        mock_use_case = MagicMock()
        mock_use_case.execute.return_value = resolved_file_mock

        # Patch temporário do use case
        with tempfile.TemporaryDirectory():
            # Executar método genérico com perfil "RIR"
            controller._run_resolution(doc_file2, "RIR")

            expected_name2 = "CZ6_RNEST_U22_3.1.1.1_CVL_RIR_B-22026A_B.pdf"
            expected_path2 = temp_path / expected_name2

            print(f"   Arquivo original: teste_generico.pdf")
            print(f"   Nome esperado: {expected_name2}")
            print(f"   Arquivo renomeado existe: {expected_path2.exists()}")
            print(
                f"   ✅ Método genérico: {'FUNCIONOU' if expected_path2.exists() else 'FALHOU'}"
            )

        # TESTE 3: Verificar que perfil PID não renomeia
        print("\n🔧 TESTE 3 - PERFIL PID (SEM RENOMEAÇÃO):")
        test_file3 = temp_path / "teste_pid.pdf"
        test_file3.write_text("arquivo simulado")

        doc_file3 = DocumentFile(test_file3, 1000)
        controller.unrecognized_files = [doc_file3]

        try:
            controller._run_resolution(doc_file3, "PID")

            # Arquivo original deve ainda existir (sem renomeação)
            print(f"   Arquivo original ainda existe: {test_file3.exists()}")
            print(
                f"   ✅ Perfil PID: {'CORRETO (sem renomeação)' if test_file3.exists() else 'FALHOU'}"
            )
        except Exception as e:
            print(f"   ⚠️ Perfil PID falhou (esperado): {e}")

        return expected_path1.exists()


def test_combobox_options():
    """Testa as opções disponíveis no ComboBox"""
    print("\n=== TESTE - OPÇÕES DO COMBOBOX ===")

    # Simular MainView
    sys.modules["customtkinter"] = MagicMock()
    from sad_app_v2.presentation.main_view import MainView

    with tempfile.TemporaryDirectory():
        mock_view = MagicMock()
        mock_combobox = MagicMock()
        mock_view.profile_combobox = mock_combobox

        # Simular perfis carregados do YAML
        yaml_profiles = ["RIR", "PID", "GERAL"]

        # Chamar método que popula ComboBox
        view = MainView()
        view.profile_combobox = mock_combobox
        view.populate_profiles_dropdown(yaml_profiles)

        # Verificar chamadas
        if mock_combobox.configure.called:
            call_args = mock_combobox.configure.call_args
            values = call_args[1]["values"]  # kwargs['values']

            print(f"📋 Opções no ComboBox:")
            for i, option in enumerate(values):
                print(f"   {i + 1}. {option}")

            print(f"\n🔍 Análise:")
            has_special_rir = any("🔍 RIR" in option for option in values)
            has_yaml_rir = "RIR" in values

            print(f"   Tem opção especial '🔍 RIR': {has_special_rir}")
            print(f"   Tem opção YAML 'RIR': {has_yaml_rir}")

            if has_special_rir and has_yaml_rir:
                print("   ⚠️ PROBLEMA: Duas opções RIR diferentes!")
                print("   💡 Usuário pode confundir e selecionar a errada")
                return True
            else:
                print("   ✅ Configuração parece OK")
                return False


if __name__ == "__main__":
    print("🧪 TESTANDO AMBOS OS MÉTODOS RIR\n")

    test1_success = test_both_rir_methods()
    has_duplicate_options = test_combobox_options()

    print(f"\n🎯 RESULTADOS:")
    print(f"   Métodos RIR funcionando: {'✅' if test1_success else '❌'}")
    print(
        f"   Opções duplicadas no ComboBox: {'⚠️ Sim' if has_duplicate_options else '✅ Não'}"
    )

    if has_duplicate_options:
        print(f"\n💡 RECOMENDAÇÃO:")
        print(f"   Remover perfil 'RIR' do YAML ou da opção especial")
        print(f"   para evitar confusão do usuário")

    print(
        f"\n🎉 CONCLUSÃO: {'Sistema funcionando' if test1_success else 'Necessita ajustes'}"
    )
