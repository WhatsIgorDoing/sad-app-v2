"""
Correções críticas para problemas de renomeação e interface
"""

import os
import shutil
from pathlib import Path
from typing import Optional


class SafeFileRenamer:
    """
    Classe para renomeação segura de arquivos com verificações completas
    """

    @staticmethod
    def _generate_unique_filename(target_path: Path) -> Path:
        """
        Gera um nome de arquivo único se o destino já existir

        Args:
            target_path: Caminho de destino desejado

        Returns:
            Path: Caminho único (pode ser o mesmo se não houver conflito)
        """
        if not target_path.exists():
            return target_path

        # Extrair componentes do nome
        stem = target_path.stem
        suffix = target_path.suffix
        parent = target_path.parent

        # Tentar gerar nomes únicos com numeração
        counter = 1
        while counter <= 1000:  # Limite de segurança
            new_name = f"{stem}_{counter:03d}{suffix}"
            new_path = parent / new_name

            if not new_path.exists():
                return new_path

            counter += 1

        # Se não conseguir gerar nome único, usar timestamp
        import time

        timestamp = int(time.time())
        new_name = f"{stem}_{timestamp}{suffix}"
        return parent / new_name

    @staticmethod
    def safe_rename_file(source_path: Path, target_path: Path) -> tuple[bool, Path]:
        """
        Renomeia um arquivo de forma segura com verificações completas

        Args:
            source_path: Caminho do arquivo original
            target_path: Caminho de destino

        Returns:
            tuple[bool, Path]: (True se sucesso, caminho final do arquivo)

        Raises:
            FileNotFoundError: Se arquivo original não existe
            PermissionError: Se não há permissão para operação
            OSError: Para outros erros do sistema
        """

        # 1. Verificações de segurança PRÉ-OPERAÇÃO
        if not source_path.exists():
            raise FileNotFoundError(f"Arquivo origem não encontrado: {source_path}")

        if not source_path.is_file():
            raise ValueError(f"Origem não é um arquivo: {source_path}")

        # 2. Gerar nome único se necessário
        unique_target_path = SafeFileRenamer._generate_unique_filename(target_path)

        if unique_target_path != target_path:
            print(
                f"⚠️ Arquivo destino já existe, usando nome único: {unique_target_path.name}"
            )

        # Verificar se diretório pai do destino existe, criar se necessário
        unique_target_path.parent.mkdir(parents=True, exist_ok=True)

        # Verificar permissões
        if not os.access(source_path.parent, os.W_OK):
            raise PermissionError(
                f"Sem permissão para escrever em: {source_path.parent}"
            )

        if not os.access(unique_target_path.parent, os.W_OK):
            raise PermissionError(
                f"Sem permissão para escrever em: {unique_target_path.parent}"
            )

        # 2. Backup do estado original
        original_size = source_path.stat().st_size

        try:
            # 3. Executar renomeação
            source_path.rename(unique_target_path)

            # 4. Verificações de segurança PÓS-OPERAÇÃO
            if not unique_target_path.exists():
                # CRÍTICO: Arquivo não foi criado!
                raise OSError(
                    f"ERRO CRÍTICO: Arquivo não foi criado em {unique_target_path}"
                )

            if source_path.exists():
                # CRÍTICO: Arquivo original ainda existe!
                raise OSError(
                    f"ERRO CRÍTICO: Arquivo original ainda existe em {source_path}"
                )

            # Verificar integridade do arquivo
            new_size = unique_target_path.stat().st_size
            if new_size != original_size:
                raise OSError(
                    f"ERRO CRÍTICO: Tamanho mudou! Original: {original_size}, "
                    f"Novo: {new_size}"
                )

            return True, unique_target_path

        except Exception as e:
            # 5. Em caso de erro, verificar estado dos arquivos
            error_info = []

            if source_path.exists():
                error_info.append(f"Arquivo original ainda existe: {source_path}")
            else:
                error_info.append(
                    f"CRÍTICO: Arquivo original desapareceu: {source_path}"
                )

            if unique_target_path.exists():
                error_info.append(f"Arquivo destino foi criado: {unique_target_path}")
                # Tentar remover arquivo parcialmente criado
                try:
                    unique_target_path.unlink()
                    error_info.append("Arquivo destino parcial removido")
                except:
                    error_info.append(
                        "AVISO: Não foi possível remover arquivo destino parcial"
                    )

            # Re-lançar exceção com informações detalhadas
            error_msg = f"Falha na renomeação: {e}\nEstado dos arquivos:\n" + "\n".join(
                error_info
            )
            raise OSError(error_msg) from e

    @staticmethod
    def safe_copy_then_delete(
        source_path: Path, target_path: Path
    ) -> tuple[bool, Path]:
        """
        Alternativa mais segura: copia arquivo e depois deleta original
        Mais lento mas mais seguro para arquivos críticos

        Returns:
            tuple[bool, Path]: (True se sucesso, caminho final do arquivo)
        """

        # Verificações iniciais
        if not source_path.exists():
            raise FileNotFoundError(f"Arquivo origem não encontrado: {source_path}")

        # Gerar nome único se necessário
        unique_target_path = SafeFileRenamer._generate_unique_filename(target_path)

        if unique_target_path != target_path:
            print(
                f"⚠️ Arquivo destino já existe, usando nome único: {unique_target_path.name}"
            )

        # Backup do estado original
        original_size = source_path.stat().st_size
        original_hash = None

        # Para arquivos pequenos, calcular hash para verificação
        if original_size < 50 * 1024 * 1024:  # 50MB
            import hashlib

            with open(source_path, "rb") as f:
                original_hash = hashlib.md5(f.read()).hexdigest()

        try:
            # 1. Copiar arquivo
            unique_target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, unique_target_path)

            # 2. Verificar cópia
            if not unique_target_path.exists():
                raise OSError("Arquivo não foi copiado")

            new_size = unique_target_path.stat().st_size
            if new_size != original_size:
                raise OSError(
                    f"Tamanho incorreto após cópia: {original_size} -> {new_size}"
                )

            # Verificar hash se calculado
            if original_hash:
                with open(unique_target_path, "rb") as f:
                    new_hash = hashlib.md5(f.read()).hexdigest()
                if new_hash != original_hash:
                    raise OSError("Hash não confere - arquivo corrompido na cópia")

            # 3. Deletar original apenas após verificação completa
            source_path.unlink()

            # 4. Verificação final
            if source_path.exists():
                raise OSError("Arquivo original não foi deletado")

            return True, unique_target_path

        except Exception as e:
            # Limpeza em caso de erro
            if unique_target_path.exists():
                try:
                    unique_target_path.unlink()
                except Exception:
                    pass
            raise OSError(f"Falha na operação copy-then-delete: {e}") from e


def generate_safe_filename(
    base_name: str, revision: str, extension: str, target_dir: Path
) -> Path:
    """
    Gera um nome de arquivo seguro, evitando conflitos

    Args:
        base_name: Nome base do arquivo
        revision: Revisão do documento
        extension: Extensão do arquivo
        target_dir: Diretório de destino

    Returns:
        Path: Caminho seguro para o arquivo
    """

    # Nome preferido
    preferred_name = f"{base_name}_{revision}{extension}"
    preferred_path = target_dir / preferred_name

    if not preferred_path.exists():
        return preferred_path

    # Se já existe, adicionar contador
    counter = 1
    while True:
        alternative_name = f"{base_name}_{revision}_{counter:03d}{extension}"
        alternative_path = target_dir / alternative_name

        if not alternative_path.exists():
            return alternative_path

        counter += 1
        if counter > 999:
            raise ValueError(
                f"Muitos arquivos com nome similar: {base_name}_{revision}"
            )
