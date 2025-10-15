"""
Implementação da classe OptimizedExtractorService
"""
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from .optimization import cache_to_disk


class OptimizedExtractorService:
    """
    Serviço de extração otimizado com cache.
    Wrapper em torno do serviço de extração original com suporte a cache.
    """

    def __init__(self, config_path: Path):
        """
        Inicializa o serviço de extração otimizado.

        Args:
            config_path: Caminho para o arquivo de configuração YAML com os padrões
        """
        # Importação preguiçosa para melhorar tempo de inicialização
        from .extraction import ProfiledExtractorService

        self._extractor = ProfiledExtractorService(config_path)

    @cache_to_disk(cache_dir=".cache/extraction")
    def extract_from_file(
        self, file_path: Path, profile: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extrai dados de um arquivo com suporte a cache.

        Args:
            file_path: Caminho do arquivo
            profile: Perfil de extração a ser usado

        Returns:
            Dados extraídos do arquivo
        """
        start_time = time.time()
        result = self._extractor.extract_from_file(file_path, profile)
        elapsed = time.time() - start_time
        # Se a extração for lenta, log isso para debug
        if elapsed > 1.0:
            print(f"Extração lenta para {file_path.name}: {elapsed:.2f}s")
        return result

    def get_available_profiles(self) -> List[str]:
        """
        Retorna a lista de perfis de extração disponíveis.

        Returns:
            Lista de nomes de perfis disponíveis
        """
        return self._extractor.get_available_profiles()

    def __getattr__(self, name: str) -> Any:
        """
        Redireciona chamadas de métodos para o extrator interno.

        Args:
            name: Nome do método ou atributo

        Returns:
            Atributo ou método do extrator interno

        Raises:
            AttributeError: Se o atributo não existir no extrator interno
        """
        return getattr(self._extractor, name)
