# SAD App v2.0

**Sistema de Automação de Documentos v2.0**

Aplicação desenvolvida seguindo os princípios da **Clean Architecture** para automatizar o processamento de documentos a partir de manifestos Excel.

## 🚀 Execução Rápida

```bash
# 1. Resolver política de execução (se necessário - Windows)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 2. Ativar ambiente virtual
.venv\Scripts\Activate.ps1  # Windows PowerShell
# ou .venv\Scripts\activate.bat  # Windows CMD
# ou source .venv/bin/activate  # Linux/macOS

# 3. Executar aplicação
python run.py
```

> 💡 **Importante**: Se encontrar erro de "execução de scripts desabilitada", veja a seção [Troubleshooting](#-troubleshooting)

## 🏗️ Arquitetura

A aplicação segue o padrão **Clean Architecture** com camadas bem definidas:

```
src/
├── sad_app_v2/
│   ├── core/                      # 🎯 Domain Layer
│   │   ├── domain.py              # Entidades e Value Objects
│   │   ├── interfaces.py          # Protocolos e Contratos
│   │   ├── exceptions.py          # Exceções do Domínio
│   │   └── use_cases/             # Casos de Uso
│   │       ├── validate_batch.py  # UC-01: Validar Lote
│   │       ├── resolve_exception.py # UC-02: Resolver Não Reconhecidos
│   │       └── organize_lots.py   # UC-03: Organizar em Lotes
│   ├── infrastructure/            # 🔧 Infrastructure Layer
│   │   ├── excel_reader.py        # Adaptador para Excel
│   │   ├── file_system.py         # Sistema de Arquivos Seguro
│   │   ├── template_filler.py     # Preenchimento de Templates
│   │   ├── services.py            # Serviços de Negócio
│   │   └── extraction.py          # Extração de Metadados
│   └── presentation/              # 🖥️ Presentation Layer
│       ├── main_view.py           # Interface Gráfica Completa
│       └── view_controller.py     # Controller MVC com Threading
├── main.py                        # 🎯 Entry Point Alternativo
└── run.py                         # 🚀 Ponto de Entrada Principal
```

## ✨ Funcionalidades

### UC-01: Validar Lote de Documentos
- ✅ Carrega manifesto de documentos (arquivo Excel)
- ✅ Varre diretório de origem em busca de arquivos
- ✅ Aplica regra de negócio RN-NEW-001 (remoção de sufixos temporários)
- ✅ Classifica arquivos como válidos ou não reconhecidos
- ✅ Exibe resultados em interface gráfica moderna

### UC-02: Resolver Arquivo Não Reconhecido
- ✅ Interface para seleção de arquivos não reconhecidos
- ✅ Aplicação de perfis de extração customizados
- ✅ Resolução automática baseada em padrões
- ✅ Atualização dinâmica das listas de arquivos

### UC-03: Organizar e Gerar Lotes
- ✅ Balanceamento inteligente de lotes por número de documentos
- ✅ Criação automática de estrutura de pastas organizadas
- ✅ Geração de templates Excel preenchidos com dados
- ✅ Movimentação segura de arquivos com validação

### Interface Gráfica Completa
- 🎨 Design moderno com CustomTkinter e tema dark
- 📋 Interface com abas (Validação + Organização)
- 📁 Seleção de manifesto, diretórios e templates via dialogs
- � Barra de progresso e feedback visual em tempo real
- 📝 Sistema de logs com timestamps e níveis de severidade
- 🔄 Processamento assíncrono com threading para UI responsiva
- ⚙️ Configuração completa de parâmetros de organização

### Qualidade de Código
- 🧪 **45 testes aprovados, 1 skipped** (98% de sucesso)
- 🔍 Testes unitários para todas as camadas
- 🌐 Testes de integração end-to-end
- 📏 Linting com Ruff e formatação automática
- 🎯 Type hints completos com Python 3.13
- 📖 Documentação abrangente com docstrings

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.13+
- Windows (testado) / Linux / macOS

### Configuração do Ambiente Virtual
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows PowerShell)
# OPÇÃO 1 - Permitir execução de scripts (Administrador):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\activate

# OPÇÃO 2 - Comando direto (sem alterar política):
.venv\Scripts\Activate.ps1

# OPÇÃO 3 - Usar Command Prompt (cmd):
.venv\Scripts\activate.bat

# Ativar ambiente virtual (Linux/macOS)
source .venv/bin/activate

# Instalar dependências
pip install customtkinter==5.2.2 openpyxl==3.1.2 pytest==8.1.1 ruff==0.1.9
```

### Executar a Aplicação
```bash
# IMPORTANTE: Ativar o ambiente virtual primeiro!

# Windows PowerShell (escolha uma opção):
.venv\Scripts\Activate.ps1        # Opção mais direta
# ou
.venv\Scripts\activate.bat        # Via Command Prompt

# Linux/macOS:
source .venv/bin/activate

# Executar interface gráfica
python run.py
```

### Executar Testes
```bash
# Executar todos os testes
python -m pytest -v

# Executar testes específicos
python -m pytest tests/unit/core/ -v
python -m pytest tests/integration/ -v
```

## 🔧 Troubleshooting

### Problema: "Execução de scripts foi desabilitada" (Windows)

**Erro:**
```
.venv\Scripts\activate : O arquivo não pode ser carregado porque a execução de scripts foi desabilitada neste sistema.
```

**Soluções:**

1. **Alterar política de execução (Recomendado):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .venv\Scripts\activate
   ```

2. **Usar comando direto:**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. **Usar Command Prompt (cmd):**
   ```cmd
   .venv\Scripts\activate.bat
   ```

### Problema: "ModuleNotFoundError: No module named 'sad_app_v2'"

**Solução:**
- Certifique-se de estar no diretório correto e usar `python run.py` (não `python main.py`)
- Verifique se o ambiente virtual está ativado

### Problema: Erro de interface gráfica

**Solução:**
- Instale/atualize o CustomTkinter: `pip install --upgrade customtkinter`
- Verifique se está executando em um ambiente com interface gráfica

## 📋 Como Usar

1. **Inicie a aplicação**: Execute `python run.py`

### Aba de Validação

2. **Selecione o Manifesto**: 
   - Clique em "Selecionar..." ao lado de "Manifesto de Entrada"
   - Escolha um arquivo Excel (.xlsx/.xls) com a estrutura:
     - Coluna A: Código SAP
     - Coluna B: Descrição
     - Coluna C: Total de Páginas
     - Coluna D: Caminho do Arquivo

3. **Selecione o Diretório**: 
   - Clique em "Selecionar..." ao lado de "Pasta de Origem"
   - Escolha a pasta contendo os documentos

4. **Execute a Validação**: 
   - Clique no botão "VALIDAR LOTE"
   - Acompanhe o progresso na barra inferior
   - Visualize os resultados nas listas

5. **Resolva Arquivos Não Reconhecidos** (se houver):
   - Selecione arquivos na lista "Não Reconhecidos"
   - Escolha um perfil de extração no dropdown
   - Clique em "Resolver Selecionados"

### Aba de Organização

6. **Configure a Organização**:
   - Selecione pasta de destino para os lotes
   - Escolha template Excel master
   - Configure número máximo de documentos por lote
   - Defina padrão de nomenclatura dos lotes
   - Ajuste número de sequência inicial

7. **Execute a Organização**:
   - Clique no botão "ORGANIZAR LOTES"
   - Acompanhe o processo no log
   - Verifique os lotes criados na pasta de destino

## 🧪 Regras de Negócio

### RN-NEW-001: Normalização de Nomes de Arquivo
Remove sufixos temporários dos nomes de arquivos para correspondência:
- `documento_temp.pdf` → `documento.pdf`
- `arquivo_backup.docx` → `arquivo.docx`
- `planilha_old.xlsx` → `planilha.xlsx`

### RN-NEW-002: Estrutura do Manifesto
O manifesto Excel deve conter:
- **Coluna A**: Código SAP (identificador único)
- **Coluna B**: Descrição do documento
- **Coluna C**: Total de páginas esperado
- **Coluna D**: Nome do arquivo esperado

## 🏛️ Padrões Arquiteturais

### Clean Architecture
- **Domain Layer**: Entidades puras sem dependências externas
- **Use Cases**: Lógica de negócio orquestrada via repositórios
- **Infrastructure**: Adaptadores para tecnologias externas
- **Presentation**: Interface do usuário com padrão MVC

### Dependency Injection
- Repositórios injetados nos Use Cases
- Controllers conectam View aos Use Cases
- Fácil substituição de implementações (mocks para testes)

### SOLID Principles
- **SRP**: Cada classe tem uma responsabilidade específica
- **OCP**: Extensível via novas implementações de interfaces
- **LSP**: Substituição transparente de implementações
- **ISP**: Interfaces específicas e coesas
- **DIP**: Dependência de abstrações, não implementações

## 🔬 Estrutura de Testes

```
tests/
├── unit/                          # Testes Unitários
│   ├── core/                      # Testa entidades e use cases
│   │   ├── test_domain.py         # Entidades de domínio
│   │   ├── test_interfaces.py     # Protocolos e exceções
│   │   └── use_cases/
│   │       └── test_validate_batch.py  # Caso de uso
│   └── presentation/              # Testa controller
│       ├── test_main_view.py      # Interface gráfica
│       └── test_controller.py     # Lógica de controle
├── integration/                   # Testes de Integração
│   ├── infrastructure/            # Adaptadores
│   │   ├── test_excel_reader.py   # Leitor de Excel
│   │   └── test_file_system.py    # Sistema de arquivos
│   └── test_end_to_end.py         # Fluxo completo
└── fixtures/                      # Dados de teste
    ├── manifesto_teste.xlsx       # Manifesto de exemplo
    └── documentos_teste/          # Arquivos de exemplo
```

## 🎯 Métricas de Qualidade

- ✅ **45 testes** aprovados, **1 skipped** (98% de sucesso)
- 📊 **5 entidades** de domínio completamente testadas
- 🔧 **6 serviços** de infraestrutura validados
- 🎮 **2 controllers** com cobertura completa
- 🌐 **3 casos de uso** implementados e testados
- 🏗️ **Clean Architecture** com 4 camadas distintas
- 🧪 Cobertura de **unit tests** + **integration tests** + **end-to-end tests**

## 🚧 Próximos Desenvolvimentos

### Melhorias de Interface
- Suporte a temas personalizáveis
- Atalhos de teclado para operações principais
- Drag & drop para seleção de arquivos
- Histórico de operações recentes

### Funcionalidades Avançadas
- Suporte a múltiplos formatos de manifesto (CSV, JSON)
- Validação de integridade de arquivos (checksums)
- Relatórios de processamento em PDF
- Integração com sistemas de armazenamento em nuvem

### Melhorias Técnicas
- Cache de validações para performance
- Configurações persistentes via arquivo de settings
- Sistema de plugins para extensibilidade
- API REST para automação via scripts

## 📄 Licença

Projeto desenvolvido para automação de documentos seguindo Clean Architecture.

---

**Desenvolvido com Clean Architecture, Python 3.13, CustomTkinter e muito ☕**