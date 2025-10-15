"""
Utilitários para melhorar o carregamento e a performance da aplicação
"""
import functools
import os
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, Optional


def lazy_load(func: Callable) -> Callable:
    """
    Decorador para implementar carregamento preguiçoso (lazy loading).
    Carrega o recurso apenas na primeira vez que é necessário.
    """
    result = None
    loaded = False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal result, loaded
        if not loaded:
            result = func(*args, **kwargs)
            loaded = True
        return result

    return wrapper


def cache_to_disk(cache_dir: str = ".cache") -> Callable:
    """
    Decorador para cachear resultados em disco.
    Útil para operações custosas como extração de texto de PDFs.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Cria hash baseado nos argumentos para servir como chave de cache
            args_str = str(args) + str(kwargs)
            import hashlib

            key = hashlib.md5(args_str.encode()).hexdigest()

            # Verifica se diretório de cache existe
            cache_path = Path(cache_dir)
            cache_path.mkdir(exist_ok=True, parents=True)

            # Nome do arquivo de cache
            cache_file = cache_path / f"{func.__name__}_{key}.cache"

            # Se o cache existe, retorna o resultado do cache
            if cache_file.exists():
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        return f.read()
                except Exception:
                    pass  # Se falhar, calcula normalmente

            # Calcula e salva em cache
            result = func(*args, **kwargs)
            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(result)
            except Exception:
                pass  # Se falhar ao salvar cache, apenas retorna o resultado

            return result

        return wrapper

    return decorator


def prefetch_in_background(resource_func: Callable, *args, **kwargs) -> None:
    """
    Pré-carrega um recurso em segundo plano para uso futuro.
    Útil para carregar dados que serão necessários em breve.
    """

    def _prefetch():
        try:
            resource_func(*args, **kwargs)
        except Exception:
            pass  # Ignora erros em carregamento em segundo plano

    thread = threading.Thread(target=_prefetch, daemon=True)
    thread.start()


class ResourceManager:
    """Gerenciador de recursos para carregamento otimizado"""

    def __init__(self):
        self._resources: Dict[str, Any] = {}
        self._loading_threads: Dict[str, threading.Thread] = {}

    def register_resource(
        self, name: str, loader_func: Callable, *args, **kwargs
    ) -> None:
        """Registra um recurso para carregamento posterior"""
        self._resources[name] = {
            "loader": loader_func,
            "args": args,
            "kwargs": kwargs,
            "loaded": False,
            "data": None,
        }

    def start_loading(self, name: str) -> None:
        """Inicia o carregamento de um recurso em segundo plano"""
        if name not in self._resources or self._resources[name]["loaded"]:
            return

        def _load():
            try:
                resource = self._resources[name]
                result = resource["loader"](*resource["args"], **resource["kwargs"])
                resource["data"] = result
                resource["loaded"] = True
            except Exception as e:
                print(f"Erro ao carregar recurso {name}: {e}")

        thread = threading.Thread(target=_load, daemon=True)
        thread.start()
        self._loading_threads[name] = thread

    def get_resource(
        self, name: str, wait: bool = True, timeout: float = None
    ) -> Optional[Any]:
        """
        Obtém um recurso, carregando-o se necessário.

        Args:
            name: Nome do recurso
            wait: Se deve esperar o carregamento concluir
            timeout: Tempo máximo de espera em segundos
        """
        if name not in self._resources:
            return None

        resource = self._resources[name]

        # Se não está carregado, inicia o carregamento
        if not resource["loaded"] and name not in self._loading_threads:
            self.start_loading(name)

        # Se deve esperar e está carregando em thread
        if wait and name in self._loading_threads:
            thread = self._loading_threads[name]
            start_time = time.time()

            while thread.is_alive():
                if timeout is not None and time.time() - start_time > timeout:
                    return None
                time.sleep(0.01)

        return resource["data"] if resource["loaded"] else None


# Instância global do gerenciador de recursos
resource_manager = ResourceManager()
