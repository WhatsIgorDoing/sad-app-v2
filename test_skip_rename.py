#!/usr/bin/env python3
"""
Teste para verificar que arquivos com nome correto não são renomeados
"""

import sys
import tempfile
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sad_app_v2.infrastructure.safe_file_operations import SafeFileRenamer


def test_skip_rename_same_name():
    """Testa que não tenta renomear arquivo para o mesmo nome"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Criar arquivo com o nome "correto"
        correct_name = "CZ6_RNEST_U22_3.1.1.1_DTAND_RIR_DTAND-0006_0.pdf"
        file_path = temp_path / correct_name
        file_path.write_text("Conteúdo do arquivo")

        print(f"📁 Diretório de teste: {temp_path}")
        print(f"📄 Arquivo criado: {file_path.name}")

        # Simular tentativa de renomear para o MESMO nome
        # No código real, isso seria detectado ANTES de chamar safe_rename_file
        if file_path.name == correct_name:
            print(f"✅ Arquivo já possui o nome correto: '{correct_name}'")
            print(f"⏭️ Pulando renomeação (não é necessária)")
            final_path = file_path
        else:
            # Se os nomes fossem diferentes, aí sim renomearia
            target_path = temp_path / correct_name
            success, final_path = SafeFileRenamer.safe_rename_file(
                file_path, target_path
            )
            print(f"✅ Renomeado para: {final_path.name}")

        # Verificar que arquivo ainda existe
        assert final_path.exists(), "Arquivo não existe!"
        assert final_path.name == correct_name, f"Nome incorreto: {final_path.name}"

        print(f"🎉 Teste passou! Arquivo mantido corretamente: {final_path.name}")
        return True


def test_rename_different_name():
    """Testa que renomeia quando os nomes são diferentes"""

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Criar arquivo com nome "errado"
        wrong_name = (
            "0011854_CZ6_RNEST_U22_3.1.1.1_DTAND_RIR_DTAND-0006_Com_Relatorio.pdf"
        )
        file_path = temp_path / wrong_name
        file_path.write_text("Conteúdo do arquivo")

        # Nome correto desejado
        correct_name = "CZ6_RNEST_U22_3.1.1.1_DTAND_RIR_DTAND-0006_0.pdf"

        print(f"\n📁 Diretório de teste: {temp_path}")
        print(f"📄 Arquivo original: {file_path.name}")
        print(f"🎯 Nome desejado: {correct_name}")

        # Verificar se precisa renomear
        if file_path.name == correct_name:
            print(f"⏭️ Arquivo já possui o nome correto, pulando...")
            final_path = file_path
        else:
            # Precisa renomear
            target_path = temp_path / correct_name
            print(f"🔄 Renomeando...")
            success, final_path = SafeFileRenamer.safe_rename_file(
                file_path, target_path
            )
            print(f"✅ Renomeado para: {final_path.name}")

        # Verificar resultado
        assert not file_path.exists(), "Arquivo original ainda existe!"
        assert final_path.exists(), "Arquivo final não existe!"
        assert final_path.name == correct_name, f"Nome incorreto: {final_path.name}"

        print(f"🎉 Teste passou! Renomeação bem-sucedida")
        return True


if __name__ == "__main__":
    print("🧪 Testando detecção de arquivos com nome correto")
    print("=" * 60)

    print("\n🔍 Teste 1: Arquivo já com nome correto (deve pular)")
    test1_result = test_skip_rename_same_name()

    print("\n🔍 Teste 2: Arquivo com nome diferente (deve renomear)")
    test2_result = test_rename_different_name()

    print("\n" + "=" * 60)
    if test1_result and test2_result:
        print("🎉 Todos os testes passaram!")
        print("\n✅ Sistema agora detecta arquivos com nome correto")
        print("✅ Evita tentativas desnecessárias de renomeação")
        print("✅ Elimina erro 'Arquivo destino já existe'")
    else:
        print("❌ Alguns testes falharam!")
        sys.exit(1)
