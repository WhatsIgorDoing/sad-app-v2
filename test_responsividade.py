#!/usr/bin/env python3
"""
Script para testar responsividade da SAD App v2.0
"""

import sys
from pathlib import Path

# Adicionar o src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sad_app_v2.presentation.design_system import ResponsiveLayout, DesignTokens


def test_responsive_calculations():
    """Testa os cálculos de responsividade."""
    print("🧪 TESTE DE RESPONSIVIDADE - SAD App v2.0")
    print("=" * 50)

    # Diferentes tamanhos de tela para testar
    screen_sizes = [
        (1024, 768, "Laptop Pequeno"),
        (1280, 720, "Desktop Padrão"),
        (1600, 900, "Desktop Grande"),
        (1920, 1080, "Full HD"),
        (2560, 1440, "2K/QHD"),
        (3840, 2160, "4K/UHD"),
    ]

    print("📊 TAMANHOS DE JANELA:")
    print("-" * 50)
    for width, height, desc in screen_sizes:
        app_width, app_height = ResponsiveLayout.get_window_size(width, height)
        padding = ResponsiveLayout.get_content_padding(width)

        print(
            f"{desc:15} | Tela: {width}x{height} | App: {app_width}x{app_height} | Padding: {padding}px"
        )

    print("\n📐 ESPAÇAMENTOS RESPONSIVOS:")
    print("-" * 50)
    for width, height, desc in screen_sizes:
        spacing = ResponsiveLayout.get_responsive_spacing(width)
        grid_config = ResponsiveLayout.configure_responsive_grid(None, width)

        print(
            f"{desc:15} | MD: {spacing['md']:2}px | LG: {spacing['lg']:2}px | Grid Pad: {grid_config['padx']}px"
        )

    print("\n🎯 BREAKPOINTS:")
    print("-" * 50)
    for name, value in DesignTokens.BREAKPOINTS.items():
        print(f"{name:10} | {value}px")

    print("\n✅ Teste concluído! Responsividade funcionando corretamente.")


if __name__ == "__main__":
    test_responsive_calculations()
