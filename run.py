import sys
from pathlib import Path

# Adiciona o diretório src ao PYTHONPATH ANTES dos imports
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from sad_app_v2.main import main

if __name__ == "__main__":
    main()
