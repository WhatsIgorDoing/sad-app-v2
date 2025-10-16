"""
Teste para verificar se a funcionalidade de detecção de arquivos sem sufixo
está funcionando corretamente.

O teste simula um cenário onde um arquivo tem o nome correto
mas está sem o sufixo de revisão.
"""

import shutil
import tempfile
from pathlib import Path

from src.sad_app_v2.core.domain import DocumentStatus, ManifestItem
from src.sad_app_v2.core.use_cases.validate_batch import ValidateBatchUseCase


def create_test_files(temp_dir):
    """Cria arquivos de teste para o cenário."""
    # Criar um arquivo com nome correto mas sem sufixo
    without_suffix = Path(temp_dir) / "RIR_DOCUMENTO_TESTE.pdf"
    with open(without_suffix, "w") as f:
        f.write("Conteúdo de teste")

    # Criar um arquivo com nome incorreto para comparação
    incorrect_name = Path(temp_dir) / "ARQUIVO_INCORRETO.pdf"
    with open(incorrect_name, "w") as f:
        f.write("Conteúdo de teste")

    # Criar um arquivo já com sufixo correto
    with_suffix = Path(temp_dir) / "RIR_DOCUMENTO_TESTE_0.pdf"
    with open(with_suffix, "w") as f:
        f.write("Conteúdo de teste")

    return without_suffix, incorrect_name, with_suffix


def create_test_manifest():
    """Cria itens de manifesto para teste."""
    # Item que corresponde ao arquivo sem sufixo
    manifest_item1 = ManifestItem(
        document_code="RIR_DOCUMENTO_TESTE",
        revision="0",
        description="Documento de teste para RIR",
    )

    # Outro item qualquer para o manifesto
    manifest_item2 = ManifestItem(
        document_code="OUTRO_DOCUMENTO",
        revision="1",
        description="Outro documento qualquer",
    )

    return [manifest_item1, manifest_item2]


def test_suffix_detection():
    """Testa a detecção de arquivos sem sufixo."""
    # Criar diretório temporário para os testes
    temp_dir = tempfile.mkdtemp()

    try:
        # Criar arquivos de teste
        without_suffix, incorrect_name, with_suffix = create_test_files(temp_dir)

        # Criar manifesto de teste
        manifest_items = create_test_manifest()

        # Criar e executar o caso de uso
        use_case = ValidateBatchUseCase()
        result = use_case.execute(
            directory_path=Path(temp_dir),
            manifest_items=manifest_items,
            file_pattern="*.pdf",
        )

        # Verificar resultados
        print("\n--- Resultados do teste ---")

        # Verificar arquivos não reconhecidos
        print("\nArquivos não reconhecidos:")
        needs_suffix_found = False
        for file in result.unrecognized_files:
            print(f"  - {file.path.name} (Status: {file.status.name})")
            if (
                file.path == without_suffix
                and file.status == DocumentStatus.NEEDS_SUFFIX
            ):
                needs_suffix_found = True
                print("    ✅ Arquivo sem sufixo detectado corretamente!")
                print(
                    f"    🔍 Item do manifesto: "
                    f"{file.associated_manifest_item.document_code}"
                )

        if not needs_suffix_found:
            print("    ❌ Falha: Arquivo sem sufixo não foi marcado como NEEDS_SUFFIX")

        # Verificar arquivos validados
        print("\nArquivos validados:")
        for file in result.validated_files:
            print(f"  - {file.path.name} (Status: {file.status.name})")

        print("\n--- Fim dos resultados ---")

        # Checar se o arquivo sem sufixo foi detectado corretamente
        assert needs_suffix_found, "O arquivo sem sufixo não foi detectado corretamente"

    finally:
        # Limpar diretório temporário
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_suffix_detection()
