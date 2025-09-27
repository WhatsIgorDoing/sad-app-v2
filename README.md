# SAD App v2.0

**Sistema de Automação de Documentos v2.0**

Aplicação desenvolvida seguindo os princípios da **Clean Architecture** para automatizar o processamento de documentos a partir de manifestos Excel.

## 🏗️ Arquitetura

A aplicação segue o padrão **Clean Architecture** com camadas bem definidas:

```
src/
├── sad_app_v2/
│   ├── core/                      # 🎯 Domain Layer
│   │   ├── domain.py              # Entidades e Value Objects
│   │   ├── interfaces.py          # Protocolos e Exceções
│   │   └── use_cases/             # Casos de Uso
│   │       └── validate_batch.py  # UC-01: Validar Lote
│   ├── infrastructure/            # 🔧 Infrastructure Layer
│   │   ├── excel_reader.py        # Adaptador para Excel
│   │   └── file_system.py         # Adaptador para Sistema de Arquivos
│   └── presentation/              # 🖥️ Presentation Layer
│       ├── main_view.py           # Interface Gráfica (CustomTkinter)
│       └── controller.py          # Controller MVC
main.py                            # 🚀 Ponto de Entrada
```

## ✨ Funcionalidades

### UC-01: Validar Lote de Documentos
- ✅ Carrega manifesto de documentos (arquivo Excel)
- ✅ Varre diretório de origem em busca de arquivos
- ✅ Aplica regra de negócio RN-NEW-001 (remoção de sufixos temporários)
- ✅ Classifica arquivos como válidos ou não reconhecidos
- ✅ Exibe resultados em interface gráfica moderna

### Interface Gráfica
- 🎨 Design moderno com CustomTkinter
- 📁 Seleção de manifesto e diretório via dialogs
- 📊 Visualização em tempo real do progresso
- 📋 Listas separadas para arquivos válidos e não reconhecidos
- 📝 Log de operações com timestamps
- 🔄 Processamento assíncrono sem travamento da interface

### Qualidade de Código
- 🧪 **100% de cobertura de testes** (16 testes aprovados)
- 🔍 Testes unitários para todas as camadas
- 🌐 Testes de integração end-to-end
- 📏 Linting com Ruff
- 🎯 Type hints completos
- 📖 Documentação abrangente

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.13+
- Windows (testado) / Linux / macOS

### Dependências
```bash
# Instalar dependências
pip install customtkinter==5.2.2 openpyxl==3.1.2 pytest==8.1.1 ruff==0.1.9
```

### Executar a Aplicação
```bash
# Executar interface gráfica
python main.py
```

### Executar Testes
```bash
# Executar todos os testes
python -m pytest -v

# Executar testes específicos
python -m pytest tests/unit/core/ -v
python -m pytest tests/integration/ -v
```

## 📋 Como Usar

1. **Inicie a aplicação**: Execute `python main.py`

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
   - Visualize os resultados nas abas

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

- ✅ **16 testes** aprovados (100% de sucesso)
- 📊 **5 entidades** de domínio testadas
- 🔧 **2 adaptadores** de infraestrutura validados
- 🎮 **1 controller** com cobertura completa
- 🌐 **2 testes** end-to-end para fluxos principais

## 🚧 Próximos Desenvolvimentos

### UC-02: Resolver Arquivo Não Reconhecido
- Interface para resolução manual de arquivos
- Sugestões automáticas baseadas em similaridade
- Histórico de resoluções

### UC-03: Organizar e Gerar Lotes
- Organização automática de arquivos em lotes
- Geração de relatórios de processamento
- Exportação de resultados

### Melhorias Técnicas
- Cache de validações para performance
- Logs estruturados com níveis
- Configurações via arquivo de settings
- Suporte a múltiplos formatos de manifesto

## 📄 Licença

Projeto desenvolvido para automação de documentos seguindo Clean Architecture.

---

**Desenvolvido com Clean Architecture, Python 3.13, CustomTkinter e muito ☕**