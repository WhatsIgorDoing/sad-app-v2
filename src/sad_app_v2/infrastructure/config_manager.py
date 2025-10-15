"""
Sistema de gerenciamento de configuração com suporte a cache.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict

from .optimization import cache_to_disk


class ConfigManager:
    """Gerenciador de configurações da aplicação com suporte a cache."""

    def __init__(self, config_dir: Path):
        """
        Inicializa o gerenciador de configurações.

        Args:
            config_dir: Diretório onde as configurações estão armazenadas
        """
        self.config_dir = config_dir
        self._cache = {}
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """Garante que o diretório de configuração existe."""
        os.makedirs(self.config_dir, exist_ok=True)

    @cache_to_disk(cache_dir=".cache/config")
    def load_config(self, name: str) -> Dict[str, Any]:
        """
        Carrega configuração de arquivo com cache em disco.

        Args:
            name: Nome do arquivo de configuração (sem extensão)

        Returns:
            Dados de configuração
        """
        config_path = self.config_dir / f"{name}.json"
        if not config_path.exists():
            return {}

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_config(self, name: str, config_data: Dict[str, Any]) -> None:
        """
        Salva configuração em arquivo.

        Args:
            name: Nome do arquivo de configuração (sem extensão)
            config_data: Dados de configuração a serem salvos
        """
        config_path = self.config_dir / f"{name}.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)

    def get_setting(self, config_name: str, key: str, default: Any = None) -> Any:
        """
        Obtém uma configuração específica.

        Args:
            config_name: Nome do arquivo de configuração
            key: Chave da configuração
            default: Valor padrão caso a configuração não exista

        Returns:
            Valor da configuração ou valor padrão
        """
        config = self.load_config(config_name)
        return config.get(key, default)

    def set_setting(self, config_name: str, key: str, value: Any) -> None:
        """
        Define uma configuração específica.

        Args:
            config_name: Nome do arquivo de configuração
            key: Chave da configuração
            value: Valor da configuração
        """
        config = self.load_config(config_name)
        config[key] = value
        self.save_config(config_name, config)
