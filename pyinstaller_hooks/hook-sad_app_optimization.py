"""
Hook de otimização personalizado para SAD App v2.0
Este arquivo ajuda o PyInstaller a otimizar o build
"""

# Configurações para reduzir o tamanho e melhorar performance
hiddenimports = [
    # Core essencial apenas
    "customtkinter",
    "tkinter",
    "openpyxl",
    "docx",
    "PyPDF2",
    "yaml",
]

# Módulos a excluir para reduzir tamanho
excludedimports = [
    "test",
    "tests",
    "unittest",
    "pytest",
    "nose",
    "PIL",
    "numpy",
    "pandas",
    "matplotlib",
    "scipy",
    "requests",
    "urllib3",
    "selenium",
    "django",
    "flask",
]


# Otimizações de coleta de dados
def get_hook_config():
    return {
        "optimize_imports": True,
        "exclude_system_libraries": True,
        "minimize_stdlib": True,
        "compress_pycs": True,
    }
