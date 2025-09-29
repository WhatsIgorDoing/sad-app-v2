import sys
from pathlib import Path

# Adiciona o diretório src ao PYTHONPATH
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Agora pode importar a aplicação
from sad_app_v2.main import main

if __name__ == "__main__":
    main()
