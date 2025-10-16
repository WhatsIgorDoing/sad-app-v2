"""
Teste simplificado para simular como a função detecta arquivos sem sufixo
"""

from pathlib import Path
from src.sad_app_v2.core.domain import DocumentStatus, DocumentFile, ManifestItem


def test_needs_suffix_detection():
    """
    Simula a verificação de um arquivo que precisa de sufixo.
    """
    print("\n--- Teste de detecção de arquivo sem sufixo ---")

    # Simular um arquivo sem sufixo
    file_path = Path("RIR_DOCUMENTO_TESTE.pdf")

    # Criar um item de manifesto correspondente
    manifest_item = ManifestItem(
        document_code="RIR_DOCUMENTO_TESTE",
        revision="0",
        title="Documento de teste para RIR",
    )

    # Criar um arquivo de documento
    file = DocumentFile(
        path=file_path,
        size_bytes=1024,  # Tamanho simulado
        status=DocumentStatus.UNRECOGNIZED,
    )

    # Simular a lógica de detecção de arquivo sem sufixo
    # Esta é uma versão simplificada do que acontece em ValidateBatchUseCase

    # Verificar se o nome do arquivo (sem extensão) corresponde exatamente
    # ao código do documento no manifesto
    file_name = file.path.stem  # Nome sem extensão

    if file_name == manifest_item.document_code:
        print(
            f"✅ Correspondência encontrada: '{file_name}' = '{manifest_item.document_code}'"
        )
        print(
            f"⚠️ Arquivo não tem sufixo. Deve ser renomeado para '{file_name}_{manifest_item.revision}{file.path.suffix}'"
        )

        # Atualizar o status do arquivo
        file.status = DocumentStatus.NEEDS_SUFFIX
        file.associated_manifest_item = manifest_item

        print(f"✅ Status atualizado: {file.status}")
        print(
            f"✅ Item do manifesto associado: {file.associated_manifest_item.document_code}"
        )

        # Agora o controlador poderia pegar este arquivo e aplicar a renomeação
        print(
            f"→ Próximo passo: Renomear para '{file_name}_{manifest_item.revision}{file.path.suffix}'"
        )
    else:
        print(f"❌ Não corresponde: '{file_name}' != '{manifest_item.document_code}'")

    print("--- Fim do teste ---")


if __name__ == "__main__":
    test_needs_suffix_detection()
