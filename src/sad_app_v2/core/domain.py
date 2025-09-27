import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


# Enum para o status dos arquivos, garantindo consistência.
class DocumentStatus(enum.Enum):
    UNVALIDATED = "Não Validado"
    VALIDATED = "Validado"
    UNRECOGNIZED = "Não Reconhecido"
    ERROR = "Erro"

@dataclass
class ManifestItem:
    """Representa uma linha do manifesto de entrada (a fonte da verdade)."""
    document_code: str
    revision: str
    title: str
    # Usamos um dicionário para metadados extras para flexibilidade.
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DocumentFile:
    """Representa um arquivo físico no disco."""
    path: Path
    size_bytes: int
    status: DocumentStatus = DocumentStatus.UNVALIDATED
    # A associação é feita após a validação bem-sucedida.
    associated_manifest_item: Optional[ManifestItem] = None

    def __post_init__(self):
        # Garante que o path seja sempre um objeto Path.
        if not isinstance(self.path, Path):
            self.path = Path(self.path)
