#!/usr/bin/env python3
"""
Script para documentar a interface do SAD App v2.0
Captura screenshots das principais telas e funcionalidades
"""

import time
from pathlib import Path

import customtkinter as ctk


def create_documentation_screenshots():
    """Cria screenshots documentados da aplicação."""

    # Nota: Este script serve como template para documentação
    # Screenshots reais devem ser capturados manualmente ou com ferramentas específicas

    print("📸 Guia para Captura de Screenshots do SAD App v2.0")
    print("=" * 60)

    screenshots_needed = [
        {
            "filename": "01_tela_principal.png",
            "description": "Tela principal da aplicação ao iniciar",
            "instructions": [
                "1. Execute: py run.py",
                "2. Aguarde a interface carregar",
                "3. Capture a tela completa",
                "4. Foque na área principal com manifesto e pasta",
            ],
        },
        {
            "filename": "02_selecao_manifesto.png",
            "description": "Diálogo de seleção de manifesto Excel",
            "instructions": [
                "1. Clique em 'Selecionar Manifesto...'",
                "2. Aguarde o diálogo abrir",
                "3. Capture o diálogo de seleção de arquivo",
                "4. Mostre filtros .xlsx e .xls",
            ],
        },
        {
            "filename": "03_exemplo_manifesto.png",
            "description": "Exemplo de estrutura do manifesto Excel",
            "instructions": [
                "1. Abra Excel com manifesto exemplo",
                "2. Mostre colunas A, B, C, D claramente",
                "3. Inclua dados de exemplo realistas",
                "4. Destaque cabeçalhos das colunas",
            ],
        },
        {
            "filename": "04_selecao_pasta.png",
            "description": "Seleção da pasta de documentos",
            "instructions": [
                "1. Clique em 'Selecionar Pasta...'",
                "2. Navegue até pasta com documentos",
                "3. Mostre conteúdo da pasta (PDFs, DOCXs)",
                "4. Capture diálogo de seleção de pasta",
            ],
        },
        {
            "filename": "05_aba_validacao.png",
            "description": "Aba de Validação e Resolução ativa",
            "instructions": [
                "1. Certifique-se de estar na aba 'Validação'",
                "2. Mostre botão 'VALIDAR LOTE' em destaque",
                "3. Inclua listas vazias (antes da validação)",
                "4. Destaque área de logs inferior",
            ],
        },
        {
            "filename": "06_processo_validacao.png",
            "description": "Processo de validação em andamento",
            "instructions": [
                "1. Clique em 'VALIDAR LOTE'",
                "2. Capture durante o processamento",
                "3. Mostre barra de progresso ativa",
                "4. Inclua logs sendo atualizados",
            ],
        },
        {
            "filename": "07_resultados_validacao.png",
            "description": "Resultados da validação completa",
            "instructions": [
                "1. Aguarde validação terminar",
                "2. Mostre lista 'Arquivos Validados' preenchida",
                "3. Mostre lista 'Não Reconhecidos' com checkboxes",
                "4. Destaque contadores nas listas",
            ],
        },
        {
            "filename": "08_resolucao_arquivos.png",
            "description": "Resolução de arquivos não reconhecidos",
            "instructions": [
                "1. Marque alguns checkboxes na lista direita",
                "2. Selecione perfil de extração (ex: RIR)",
                "3. Mostre botão 'Resolver Selecionados' ativo",
                "4. Destaque dropdown de perfis",
            ],
        },
        {
            "filename": "09_aba_organizacao.png",
            "description": "Aba de Organização e Saída",
            "instructions": [
                "1. Clique na aba '2. Organização e Saída'",
                "2. IMPORTANTE: Mostre botão mudou para 'ORGANIZAR E GERAR LOTES'",
                "3. Destaque cor verde do botão",
                "4. Mostre formulário de configuração",
            ],
        },
        {
            "filename": "10_configuracoes_organizacao.png",
            "description": "Configurações da organização preenchidas",
            "instructions": [
                "1. Preencha pasta de destino",
                "2. Selecione template master",
                "3. Configure máximo de documentos (ex: 50)",
                "4. Ajuste padrão de nomenclatura",
            ],
        },
        {
            "filename": "11_processo_organizacao.png",
            "description": "Processo de organização em andamento",
            "instructions": [
                "1. Clique em 'ORGANIZAR E GERAR LOTES'",
                "2. Capture durante o processamento",
                "3. Mostre logs de criação de lotes",
                "4. Destaque barra de progresso",
            ],
        },
        {
            "filename": "12_estrutura_lotes.png",
            "description": "Estrutura de pastas dos lotes criados",
            "instructions": [
                "1. Abra Windows Explorer",
                "2. Navegue até pasta de destino",
                "3. Mostre pastas LOTE-0001, LOTE-0002, etc.",
                "4. Entre em um lote e mostre conteúdo",
            ],
        },
        {
            "filename": "13_logs_sistema.png",
            "description": "Sistema de logs em detalhes",
            "instructions": [
                "1. Foque na área de logs inferior",
                "2. Mostre diferentes tipos de mensagem",
                "3. Inclua timestamps e ícones",
                "4. Destaque scrollbar se necessário",
            ],
        },
        {
            "filename": "14_botao_dinamico.png",
            "description": "Demonstração do botão dinâmico",
            "instructions": [
                "1. Capture lado a lado: aba validação vs organização",
                "2. Destaque mudança do botão principal",
                "3. Mostre cores diferentes (azul vs verde)",
                "4. Inclua setas indicativas",
            ],
        },
    ]

    # Criar pasta para screenshots
    screenshots_dir = Path("docs/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Pasta para screenshots: {screenshots_dir}")
    print(f"📸 {len(screenshots_needed)} screenshots necessários\n")

    # Listar todas as capturas necessárias
    for i, shot in enumerate(screenshots_needed, 1):
        print(f"{i:2d}. {shot['filename']}")
        print(f"    📝 {shot['description']}")
        print("    📋 Instruções:")
        for instruction in shot["instructions"]:
            print(f"       {instruction}")
        print()

    # Criar arquivo README para screenshots
    readme_content = f"""# Screenshots do SAD App v2.0

Esta pasta contém os screenshots da interface do usuário para documentação.

## Lista de Screenshots Necessários

{chr(10).join([f"{i}. **{shot['filename']}** - {shot['description']}" for i, shot in enumerate(screenshots_needed, 1)])}

## Como Usar

1. Execute a aplicação: `py run.py`
2. Siga as instruções para cada screenshot
3. Use ferramenta de captura de tela (Snipping Tool, etc.)
4. Salve com o nome exato especificado
5. Otimize imagens para web (PNG, < 500KB cada)

## Dicas para Screenshots

- **Resolução**: Use resolução padrão (1280x720 ou superior)
- **Qualidade**: PNG com boa qualidade mas otimizado
- **Foco**: Destaque elementos importantes com bordas ou setas
- **Consistência**: Mantenha mesmo tema e tamanho de janela
- **Legibilidade**: Certifique-se que texto seja legível

## Ferramentas Recomendadas

- **Windows**: Snipping Tool, Print Screen
- **Edição**: Paint, GIMP, ou editor simples
- **Otimização**: TinyPNG, OptiPNG

---

*Gerado automaticamente para documentação do SAD App v2.0*
"""

    readme_path = screenshots_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✅ Arquivo README criado: {readme_path}")
    print("\n🎯 Próximos passos:")
    print("1. Execute a aplicação")
    print("2. Siga as instruções para cada screenshot")
    print("3. Capture e salve as imagens")
    print("4. Atualize o GUIA_DE_USO.md com as imagens")


if __name__ == "__main__":
    create_documentation_screenshots()
