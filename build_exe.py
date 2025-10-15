#!/usr/bin/env python3
"""
Script para construir o executável do SAD App v2.0
Configurações otimizadas para PyInstaller
"""

import subprocess
import sys
from pathlib import Path


def build_executable():
    """Constrói o executável usando PyInstaller."""

    # Diretório do projeto
    project_dir = Path(__file__).parent

    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--name=SAD_App_v2",  # Nome do executável
        "--onefile",  # Arquivo único
        "--windowed",  # Interface gráfica
        "--add-data=config;config",  # Incluir pasta config
        "--add-data=src;src",  # Incluir código fonte
        "--hidden-import=customtkinter",  # Imports explícitos
        "--hidden-import=tkinter",
        "--hidden-import=openpyxl",
        "--hidden-import=docx",
        "--hidden-import=PyPDF2",
        "--hidden-import=yaml",
        "--collect-all=customtkinter",  # Coletar CustomTkinter
        "--noconfirm",  # Não perguntar confirmação
        "--clean",  # Limpar cache
        "run.py",  # Arquivo principal
    ]

    print("🚀 Iniciando construção do executável...")
    print(f"Comando: {' '.join(cmd)}")

    try:
        # Executar PyInstaller
        subprocess.run(cmd, cwd=project_dir, check=True, capture_output=True, text=True)

        print("✅ Executável criado com sucesso!")
        print(f"📁 Localização: {project_dir / 'dist' / 'SAD_App_v2.exe'}")

        # Mostrar tamanho do arquivo
        exe_path = project_dir / "dist" / "SAD_App_v2.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📊 Tamanho: {size_mb:.1f} MB")

    except subprocess.CalledProcessError as e:
        print("❌ Erro ao criar executável:")
        print(e.stdout)
        print(e.stderr)
        return False

    return True


def create_simple_spec():
    """Cria um arquivo .spec simples caso seja necessário personalizar mais."""

    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'customtkinter',
        'tkinter',
        'openpyxl',
        'docx',
        'PyPDF2',
        'yaml',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SAD_App_v2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='config/app_icon.ico'  # Remova se não tiver ícone
)
"""

    with open("SAD_App_v2.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)

    print("📝 Arquivo SAD_App_v2.spec criado para customizações avançadas")


if __name__ == "__main__":
    print("🏗️  SAD App v2.0 - Construtor de Executável")
    print("=" * 50)

    # Verificar se estamos no ambiente virtual
    if not hasattr(sys, "real_prefix") and not sys.base_prefix != sys.prefix:
        print("⚠️  AVISO: Execute este script dentro do ambiente virtual!")
        print("Execute: .venv\\Scripts\\Activate.ps1")
        sys.exit(1)

    # Construir executável
    success = build_executable()

    if success:
        print("\n🎉 Processo concluído!")
        print("\n📋 Próximos passos:")
        print("1. Teste o executável: dist/SAD_App_v2.exe")
        print("2. O arquivo pode ser distribuído independentemente")
        print("3. Não é necessário instalar Python no computador de destino")
    else:
        print("\n❌ Falha na construção do executável")
        print("Verifique os erros acima e tente novamente")
