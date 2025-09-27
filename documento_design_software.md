# Documento de Design de Software (DDS) - SAD

**Versão:** 1.0  
**Data:** 27 de Setembro de 2025

## 1.0 Introdução e Visão Geral

### 1.1 Objetivo do Documento

Este documento detalha o design técnico e os requisitos funcionais para o desenvolvimento do SAD. Ele serve como a fonte única da verdade para a equipe de desenvolvimento, garantindo que a lógica de negócio, a arquitetura e a experiência do usuário sejam implementadas conforme o planejado.

### 1.2 Escopo do Sistema

O SAD App v2.0 é uma suíte de automação de preparação de lotes de entrega de documentos. Suas responsabilidades principais são:

- Validar um lote de arquivos de entrada contra um manifesto mestre (planilha Excel).
- Fornecer um assistente para identificar e corrigir arquivos não reconhecidos através de perfis de extração de conteúdo.
- Organizar os arquivos validados em lotes de saída, aplicando regras de balanceamento de tamanho.
- Gerar manifestos de lote padronizados a partir de um template mestre para cada lote de saída.

### 1.3 Declaração do Problema de Negócio

O processo manual de validar, renomear, organizar e documentar grandes volumes de arquivos de projeto é lento, propenso a erros e carece de rastreabilidade, tornando as entregas e auditorias ineficientes.

## 2.0 Arquitetura do Sistema

### 2.1 Paradigma Arquitetural: Clean Architecture

O sistema será construído seguindo os princípios da Clean Architecture para garantir:

- **Independência de Frameworks e UI:** A lógica de negócio não depende de detalhes de implementação.
- **Testabilidade:** As regras de negócio podem ser testadas isoladamente.
- **Manutenibilidade:** As camadas podem ser modificadas sem impactar as outras.

### 2.2 Diagrama de Camadas

```
+-------------------------------------------------------------+
| Camada de Apresentação (GUI - CustomTkinter)                |
|       [Controllers, ViewModels, Views]                      |
+-----------------------+-------------------------------------+
                        | (Chama Casos de Uso)
+-----------------------v-------------------------------------+
| Camada de Domínio e Aplicação (Core - Python Puro)          |
|                                                             |
|   +-----------------+   +-------------------------------+   |
|   |    Entidades    |   |         Casos de Uso          |   |
|   | (ManifestItem,  |   | (ValidateBatch, ResolveFile,  |   |
|   |  Documento...)  |   |    OrganizeLots...)           |   |
|   +-----------------+   +---------------+---------------+   |
|                                         |                   |
|   +-------------------------------------v----------------+  |
|   |     Interfaces de Repositório (Abstrações/Ports)     |  |
|   | (IManifestReader, IFileMatcher, ITemplateFiller...)  |  |
|   +------------------------------------------------------+  |
+-----------------------+-------------------------------------+
                        | (Implementado por)
+-----------------------v-------------------------------------+
| Camada de Infraestrutura (Adapters - Bibliotecas Externas)  |
|   (Leitor de Excel, File System API, Preenchedor de Excel)  |
+-------------------------------------------------------------+
```

## 3.0 Modelo de Domínio (Core)

*(Esta seção detalha as estruturas de dados puras que representam os conceitos de negócio)*

### 3.1 Entidades

**ManifestItem:** Representa uma linha do manifesto de entrada.
- `document_code` (str): A chave primária (Coluna "DOCUMENTO").
- `revision` (str): A revisão.
- `title` (str): O título do documento.
- `metadata` (dict): Um dicionário para outras colunas (DISCIPLINA, etc.).

**DocumentFile:** Representa um arquivo físico no disco.
- `path` (Path): O caminho completo para o arquivo.
- `size_bytes` (int): O tamanho do arquivo.
- `status` (Enum): UNVALIDATED, VALIDATED, UNRECOGNIZED, ERROR.
- `associated_manifest_item` (ManifestItem, optional): A ligação com o manifesto após a validação.

**OutputLot:** Representa um lote de saída.
- `lot_name` (str): O nome sequencial do lote.
- `files` (List[DocumentFile]): A lista de arquivos no lote.
- `total_size_bytes` (int): A soma dos tamanhos dos arquivos

## 4.0 Casos de Uso (Core)

*(Aqui detalhamos cada funcionalidade do sistema. Começarei com o primeiro como modelo)*

### 4.1 UC-01: Validar Lote de Documentos

- **ID:** UC-01
- **Nome:** Validar Lote de Documentos
- **Ator Primário:** Analista de Documentos
- **Resumo:** O caso de uso recebe os caminhos de uma pasta de origem e de uma planilha manifesto, e compara os dois para determinar quais arquivos são validados e quais não são reconhecidos.

**Pré-condições:**
- O caminho para a pasta de origem é válido.
- O caminho para a planilha de manifesto é válido.

**Fluxo Principal (Happy Path):**
1. O sistema é invocado com o caminho da pasta de origem e o caminho do manifesto.
2. O sistema solicita ao IManifestRepository para carregar todos os ManifestItem do arquivo Excel.
3. O sistema solicita ao IFileRepository para listar todos os DocumentFile da pasta de origem.
4. Para cada DocumentFile listado, o sistema tenta encontrar um ManifestItem correspondente usando a RN-NEW-001 (Correspondência por Nome Base).
5. Se uma correspondência for encontrada:
   - a. O status do DocumentFile é definido como VALIDATED.
   - b. O DocumentFile é associado ao ManifestItem correspondente.
6. Se nenhuma correspondência for encontrada:
   - a. O status do DocumentFile é definido como UNRECOGNIZED.
7. O sistema retorna duas listas: uma de DocumentFile validados e outra de não reconhecidos.

**Fluxos de Exceção:**
- **Exceção 4.1.A - Manifesto não encontrado/ilegível:** O caso de uso lança uma ManifestReadError.
- **Exceção 4.1.B - Pasta de origem não encontrada:** O caso de uso lança uma SourceDirectoryNotFoundError.

**Pós-condições:**
- O estado da aplicação é atualizado com a lista de arquivos validados e não reconhecidos.
- Nenhum arquivo no disco foi modificado ou movido.

**Dependências (Interfaces):**
- IManifestRepository: Para ler os dados do Excel.
- IFileRepository: Para listar os arquivos no disco.

### 4.2 UC-02: Resolver Arquivo Não Reconhecido

- **ID:** UC-02
- **Nome:** Resolver Arquivo Não Reconhecido
- **Ator Primário:** Analista de Documentos
- **Resumo:** Após a execução do UC-01, o usuário seleciona um ou mais arquivos da lista "Não Reconhecidos" e escolhe um "Perfil de Extração". O sistema tenta extrair um código de relatório do conteúdo do(s) arquivo(s) usando a lógica do perfil selecionado. Se bem-sucedido, o arquivo é validado contra o manifesto e atualizado.

**Pré-condições:**
- O caso de uso UC-01 já foi executado.
- Existe uma lista de arquivos com o status UNRECOGNIZED.
- A lista de ManifestItem (do manifesto original) está carregada na memória.

**Fluxo Principal (Happy Path):**
1. O usuário invoca o caso de uso, fornecendo uma lista de um ou mais DocumentFile (com status UNRECOGNIZED) e um ExtractionProfileID (ex: "RIR").
2. Para cada DocumentFile na lista fornecida:
   - a. O sistema solicita ao IContentExtractor para extrair o texto bruto do arquivo, usando o ExtractionProfileID para determinar a estratégia (ex: extrair texto de PDF, aplicar OCR em imagem, etc.).
   - b. O sistema solicita ao ICodeExtractor para encontrar um código de relatório no texto extraído, usando os padrões regex associados ao ExtractionProfileID.
   - c. Se um código de relatório for extraído com sucesso:
     - i. O sistema o sanitiza (remove sufixos de revisão, etc., conforme RN001).
     - ii. O sistema busca na lista de ManifestItem carregada se existe um item com este código.
     - iii. Se houver correspondência no manifesto, o sistema atualiza o DocumentFile:
       - Define o status como VALIDATED.
       - Associa-o ao ManifestItem correspondente.
       - (Opcional, a ser definido na camada de Apresentação) Sugere a renomeação do arquivo físico para o padrão correto.
3. O sistema retorna a lista de DocumentFile que foram resolvidos com sucesso.

**Fluxos de Exceção:**
- **Exceção 4.2.A - Nenhuma correspondência de código no manifesto:** A extração do código do conteúdo do arquivo é bem-sucedida, mas este código não existe na planilha manifesto. O sistema retorna um erro CodeNotInManifestError para este arquivo específico. O status do arquivo pode ser alterado para ERROR_CODE_NOT_FOUND.
- **Exceção 4.2.B - Nenhuma extração bem-sucedida:** O perfil de extração selecionado não consegue encontrar um código de relatório no conteúdo do documento. O sistema retorna um ExtractionFailedError. O status do arquivo permanece UNRECOGNIZED.
- **Exceção 4.2.C - Arquivo ilegível:** O IContentExtractor não consegue ler o conteúdo do arquivo (ex: arquivo corrompido). O sistema retorna um FileReadError. O status do arquivo é alterado para ERROR_FILE_CORRUPTED.

**Pós-condições:**
- Os arquivos resolvidos com sucesso são removidos da lista de "Não Reconhecidos" e adicionados à lista de "Validados".
- Arquivos que falharam no processo mantêm seu status UNRECOGNIZED ou são movidos para um estado de erro, com o motivo da falha registrado.
- O estado geral do lote é atualizado para refletir as mudanças.

**Dependências (Interfaces):**
- IContentExtractor: Abstração para um serviço que sabe como extrair texto de diferentes tipos de arquivos (PDF, DOCX, OCR para imagens).
- ICodeExtractor: Abstração para um serviço que recebe um texto e uma coleção de padrões (um perfil) e retorna um código de relatório.

### 4.3 UC-03: Organizar e Gerar Lotes

- **ID:** UC-03
- **Nome:** Organizar e Gerar Lotes de Saída
- **Ator Primário:** Analista de Documentos
- **Resumo:** Este caso de uso pega a lista final de arquivos validados e executa o processo completo de organização. Ele agrupa arquivos relacionados, balanceia a distribuição desses grupos em lotes de acordo com o tamanho, move os arquivos físicos para pastas de destino nomeadas sequencialmente e preenche um manifesto de lote para cada pasta de destino criada, usando um template mestre.

**Pré-condições:**
- UC-01 e, opcionalmente, UC-02 foram executados.
- Existe uma lista de DocumentFile com status VALIDATED, cada um associado a um ManifestItem.
- O usuário forneceu os parâmetros de configuração da organização:
  - `max_docs_per_lot` (int): Quantidade máxima de documentos por lote.
  - `start_sequence_number` (int): Número sequencial inicial.
  - `master_template_path` (Path): Caminho para o arquivo template Excel.
  - `output_directory` (Path): Pasta raiz onde os lotes serão criados.

**Fluxo Principal (Happy Path):**
1. O sistema é invocado com a lista de DocumentFile validados e os parâmetros de configuração.
2. **Passo 1: Agrupamento.** O sistema agrupa os DocumentFile com base no document_code do ManifestItem associado. O resultado é uma lista de DocumentGroup, onde cada grupo contém um ou mais arquivos (ex: um .pdf e um .dwg) e tem um tamanho total (soma dos tamanhos dos arquivos).
3. **Passo 2: Balanceamento.** O sistema invoca o ILotBalancerService com a lista de DocumentGroup e os parâmetros. O serviço executa a RN-NEW-006 (Algoritmo de Balanceamento "Guloso") e retorna uma estrutura de dados que define quais grupos de documentos vão para cada lote (ex: List[OutputLot]). A regra de agrupamento (RN-NEW-002) tem precedência sobre o balanceamento perfeito.
4. **Passo 3: Nomenclatura.** O sistema itera sobre os lotes definidos, aplicando a RN-NEW-008 (Nomenclatura Sequencial de Lotes) para gerar o nome final de cada pasta de destino e de cada manifesto de lote (ex: ...-0001-..., ...-0002-...).
5. **Passo 4: Operações de Arquivo.** Para cada OutputLot definido:
   - a. O sistema cria a pasta de destino com o nome sequencial na output_directory.
   - b. O sistema solicita ao IFileSystemManager que mova cada arquivo físico do DocumentGroup da sua localização original para a nova pasta de destino.
   - c. O sistema cria uma cópia do master_template_path dentro da nova pasta de destino, renomeando-a com o nome sequencial do lote.
   - d. O sistema solicita ao ITemplateFiller para preencher a cópia do template com os dados dos ManifestItem correspondentes aos arquivos naquele lote, conforme RN-NEW-007.
6. **Passo 5: Geração de Relatório.** O sistema compila um relatório final da operação, detalhando quais arquivos foram para qual lote, os tamanhos dos lotes e o status de sucesso de cada operação.
7. O sistema retorna o relatório final da operação.

**Fluxos de Exceção:**
- **Exceção 4.3.A - Falha na Movimentação de Arquivo:** O IFileSystemManager falha ao mover um arquivo (ex: disco cheio, perda de acesso à rede no meio da operação). O sistema deve tentar reverter as operações do lote atual (se possível) ou, no mínimo, registrar o erro de forma clara no relatório final, marcando o lote como "Incompleto" ou "Falhou". O sistema não deve prosseguir para o próximo lote.
- **Exceção 4.3.B - Template Mestre não encontrado:** O caminho fornecido para o template é inválido. O caso de uso lança uma TemplateNotFoundError.
- **Exceção 4.3.C - Erro no Preenchimento do Template:** O ITemplateFiller falha (ex: template corrompido, colunas esperadas não encontradas). O caso de uso lança uma TemplateFillError, registra a falha para aquele lote e continua para o próximo, se possível.

**Pós-condições:**
- Os arquivos validados foram movidos de suas pastas de origem para as novas pastas de lote.
- As pastas de lote e seus respectivos manifestos Excel foram criados no diretório de saída.
- Um relatório consolidado da operação está disponível para o usuário.

**Dependências (Interfaces):**
- ILotBalancerService: Abstração para o serviço que contém a lógica de balanceamento.
- IFileSystemManager: Abstração para operações de sistema de arquivos (criar pasta, mover arquivo, copiar arquivo).
- ITemplateFiller: Abstração para o serviço que sabe como abrir um template Excel, preencher dados e salvá-lo.

## 5.0 Interfaces de Aplicação e Infraestrutura (Core Ports)

Esta seção define as interfaces abstratas (Protocols) que a camada de Domínio e Aplicação (Core) utiliza para interagir com serviços externos, como o sistema de arquivos, leitores de planilhas e outros. As implementações concretas destas interfaces residirão na camada de Infraestrutura.

### 5.1 IManifestRepository

- **Responsabilidade:** Ler e analisar a planilha manifesto de entrada.
- **Consumido por:** UC-01: Validar Lote de Documentos.

**Definição do Contrato:**

```python
from typing import List, Protocol
from pathlib import Path
from .domain import ManifestItem # Referência à nossa entidade de domínio

class IManifestRepository(Protocol):
    """
    Interface para um repositório que lê dados de um manifesto.
    """
    def load_from_file(self, file_path: Path) -> List[ManifestItem]:
        """
        Carrega os dados de uma planilha Excel e os transforma em uma lista
        de entidades ManifestItem.

        Args:
            file_path: O caminho para o arquivo .xlsx do manifesto.

        Returns:
            Uma lista de objetos ManifestItem.

        Raises:
            ManifestReadError: Se o arquivo não puder ser lido ou estiver
                             em um formato inválido.
        """
```

### 5.2 IFileRepository

- **Responsabilidade:** Listar e obter informações de arquivos em um diretório.
- **Consumido por:** UC-01: Validar Lote de Documentos.

**Definição do Contrato:**

```python
from typing import List, Protocol
from pathlib import Path
from .domain import DocumentFile # Referência à nossa entidade de domínio

class IFileRepository(Protocol):
    """
    Interface para um repositório que interage com o sistema de arquivos
    para listar arquivos.
    """
    def list_files(self, directory: Path) -> List[DocumentFile]:
        """
        Escaneia um diretório e retorna uma lista de entidades DocumentFile
        representando os arquivos encontrados.

        Args:
            directory: O caminho para o diretório de origem.

        Returns:
            Uma lista de objetos DocumentFile.

        Raises:
            SourceDirectoryNotFoundError: Se o diretório não existir.
        """
```

### 5.3 IContentExtractor

- **Responsabilidade:** Extrair conteúdo de texto de diferentes tipos de arquivos.
- **Consumido por:** UC-02: Resolver Arquivo Não Reconhecido.

**Definição do Contrato:**

```python
from typing import Protocol
from .domain import DocumentFile

class IContentExtractor(Protocol):
    """
    Interface para um serviço que extrai conteúdo textual de um arquivo.
    """
    def extract_text(self, file: DocumentFile, profile_id: str) -> str:
        """
        Extrai o texto de um arquivo usando uma estratégia definida por um perfil.
        A implementação pode usar diferentes bibliotecas para PDF, DOCX ou
        mesmo serviços de OCR para imagens.

        Args:
            file: O objeto DocumentFile a ser processado.
            profile_id: O identificador do perfil (ex: "RIR") para selecionar
                        a estratégia correta.

        Returns:
            O conteúdo textual extraído do arquivo.

        Raises:
            FileReadError: Se o arquivo estiver corrompido ou for ilegível.
        """
```

### 5.4 ICodeExtractor

- **Responsabilidade:** Encontrar códigos de relatório em um bloco de texto usando regras de um perfil.
- **Consumido por:** UC-02: Resolver Arquivo Não Reconhecido.

**Definição do Contrato:**

```python
from typing import Optional, Protocol

class ICodeExtractor(Protocol):
    """
    Interface para um serviço que encontra um código de relatório em um texto.
    """
    def find_code(self, text: str, profile_id: str) -> Optional[str]:
        """
        Aplica um conjunto de padrões regex (definidos por um perfil) a um
        texto para encontrar um código de relatório.

        Args:
            text: O texto a ser analisado.
            profile_id: O identificador do perfil para selecionar os padrões
                        regex corretos.

        Returns:
            O código encontrado como uma string, ou None se nenhum código
            for encontrado.
        """
```

### 5.5 ILotBalancerService

- **Responsabilidade:** Implementar a lógica de negócio para balancear a distribuição de arquivos em lotes.
- **Consumido por:** UC-03: Organizar e Gerar Lotes.

**Definição do Contrato:**

```python
from typing import List, Protocol
from .domain import DocumentGroup, OutputLot

class ILotBalancerService(Protocol):
    """
    Interface para o serviço que contém a lógica de balanceamento de lotes.
    """
    def balance_lots(
        self,
        groups: List[DocumentGroup],
        max_docs_per_lot: int
    ) -> List[OutputLot]:
        """
        Recebe uma lista de grupos de documentos e os distribui em lotes,
        tentando equilibrar o tamanho total de cada lote.

        Args:
            groups: A lista de DocumentGroup a ser distribuída.
            max_docs_per_lot: O número máximo de documentos por lote.

        Returns:
            Uma lista de objetos OutputLot, definindo a estrutura final dos lotes.
        """
```

### 5.6 IFileSystemManager

- **Responsabilidade:** Executar operações físicas de manipulação de arquivos e diretórios.
- **Consumido por:** UC-03: Organizar e Gerar Lotes.

**Definição do Contrato:**

```python
from typing import Protocol
from pathlib import Path

class IFileSystemManager(Protocol):
    """
    Interface para um gerenciador de operações do sistema de arquivos.
    """
    def create_directory(self, path: Path) -> None: ...
    def move_file(self, source: Path, destination: Path) -> None: ...
    def copy_file(self, source: Path, destination: Path) -> None: ...
```

### 5.7 ITemplateFiller

- **Responsabilidade:** Preencher um arquivo template Excel com dados e salvá-lo.
- **Consumido por:** UC-03: Organizar e Gerar Lotes.

**Definição do Contrato:**

```python
from typing import List, Protocol
from pathlib import Path
from .domain import ManifestItem

class ITemplateFiller(Protocol):
    """
    Interface para um serviço que preenche um template Excel.
    """
    def fill_and_save(
        self,
        template_path: Path,
        output_path: Path,
        data: List[ManifestItem]
    ) -> None:
        """
        Abre um arquivo template, preenche com os dados fornecidos e
        salva no caminho de saída.

        Args:
            template_path: O caminho para o arquivo .xlsx mestre.
            output_path: O caminho onde o arquivo preenchido será salvo.
            data: A lista de ManifestItem com os dados a serem inseridos.

        Raises:
            TemplateNotFoundError: Se o template mestre não for encontrado.
            TemplateFillError: Se ocorrer um erro durante o preenchimento.
        """
```

## 6.0 Implementação de Infraestrutura (Adapters)

Esta seção descreve as classes concretas que implementam as interfaces definidas na Seção 5.0. Estas classes residem na camada de Infraestrutura e lidam com todas as interações com o mundo exterior (sistema de arquivos, bibliotecas de terceiros, etc.).

### 6.1 Implementação de IManifestRepository

- **Nome da Classe Concreta:** ExcelManifestRepository
- **Biblioteca Principal:** openpyxl (para manipulação de arquivos .xlsx)

**Lógica de Implementação:**
- O método `load_from_file` receberá o `file_path`.
- Usará `openpyxl.load_workbook(file_path, read_only=True)` para abrir a planilha de forma otimizada para leitura.
- Acessará a planilha ativa (`workbook.active`).
- Iterará sobre as linhas (`sheet.iter_rows`), ignorando a primeira linha (cabeçalho).
- Para cada linha, criará uma instância da entidade ManifestItem, mapeando os valores das células das colunas (`cell.value`) para os atributos da entidade (`document_code`, `title`, etc.).
- Retornará a lista completa de ManifestItem.

**Gerenciamento de Erros:**
- Capturará `FileNotFoundError` e a relançará como `ManifestReadError`.
- Capturará exceções específicas do openpyxl (ex: `InvalidFileException`) e as relançará como `ManifestReadError`.

### 6.2 Implementação de IFileRepository

- **Nome da Classe Concreta:** FileSystemFileRepository
- **Biblioteca Principal:** pathlib (nativa do Python)

**Lógica de Implementação:**
- O método `list_files` usará `Path(directory).rglob('*')` para buscar recursivamente por todos os itens no diretório.
- Para cada item encontrado, verificará se é um arquivo com `path.is_file()`.
- Para cada arquivo, obterá o tamanho em bytes com `path.stat().st_size`.
- Criará e retornará uma lista de entidades DocumentFile com os dados coletados.

**Gerenciamento de Erros:**
- Um bloco `try...except FileNotFoundError` envolverá a operação inicial para capturar o erro de diretório inválido e o relançará como `SourceDirectoryNotFoundError`.

### 6.3 Implementações de IContentExtractor e ICodeExtractor

- **Nome da Classe Concreta:** ProfiledExtractorService (implementará ambas as interfaces)
- **Bibliotecas Principais:** PyPDF2 (para PDFs), python-docx (para DOCXs), re (para Regex).

**Lógica de Implementação:**
- A classe será inicializada com uma configuração de perfis (carregada de um arquivo `patterns.yaml`). Essa configuração mapeará um `profile_id` (ex: "RIR") para uma lista de padrões regex e outras diretivas.
- `extract_text`: O método verificará a extensão do arquivo (.pdf, .docx, etc.). Com base na extensão, ele chamará um método privado que usa a biblioteca apropriada (PyPDF2 ou python-docx) para extrair o texto bruto.
- `find_code`: O método receberá o texto e o `profile_id`. Ele buscará na configuração os padrões regex para aquele perfil e os aplicará sequencialmente ao texto usando o módulo `re`. O primeiro padrão que encontrar uma correspondência retornará o código. Se nenhum corresponder, retornará None.

**Gerenciamento de Erros:**
- Capturará exceções específicas das bibliotecas (ex: `PyPDF2.errors.PdfReadError`) e as relançará como `FileReadError`.

### 6.4 Implementação de ILotBalancerService

- **Nome da Classe Concreta:** GreedyLotBalancerService
- **Biblioteca Principal:** Nenhuma (lógica pura em Python).

**Lógica de Implementação:**

O método `balance_lots` implementará exatamente o RN-NEW-006 (Algoritmo "Guloso"):
- Receberá a lista de DocumentGroup.
- Calculará o tamanho total de cada grupo.
- Ordenará a lista de grupos em ordem decrescente de tamanho.
- Inicializará uma lista de OutputLot vazia.
- Iterará sobre a lista ordenada de grupos, alocando cada grupo ao lote que atualmente tiver o menor tamanho total, sempre respeitando o `max_docs_per_lot`.
- Retornará a lista final de OutputLot.

**Gerenciamento de Erros:** Sendo lógica pura, as validações de entrada (ex: lista de grupos vazia) serão tratadas com asserções ou checagens de pré-condição.

### 6.5 Implementação de IFileSystemManager

- **Nome da Classe Concreta:** SafeFileSystemManager
- **Bibliotecas Principais:** pathlib e shutil (nativas do Python).

**Lógica de Implementação:**
- `create_directory`: Usará `path.mkdir(parents=True, exist_ok=True)` para criar diretórios de forma segura.
- `copy_file`: Usará `shutil.copy2(source, destination)` para garantir que os metadados do arquivo (como data de modificação) sejam preservados.
- `move_file`: Usará `shutil.move(source, destination)` para uma operação de movimentação robusta.

**Gerenciamento de Erros:** As operações serão envolvidas em blocos `try...except` para capturar `IOError`, `PermissionError`, etc., e relançá-las como uma exceção de domínio mais específica, como `FileSystemOperationError`.

### 6.6 Implementação de ITemplateFiller

- **Nome da Classe Concreta:** OpenpyxlTemplateFiller
- **Biblioteca Principal:** openpyxl, shutil.

**Lógica de Implementação:**
- O método `fill_and_save` primeiro usará o `SafeFileSystemManager.copy_file` para copiar o `template_path` para o `output_path`. Isso garante que o template original nunca seja modificado.
- Em seguida, usará `openpyxl.load_workbook(output_path)` para abrir a cópia recém-criada.
- Iterará sobre a lista de `data` (ManifestItem) e preencherá as células da planilha a partir da segunda linha, mapeando os atributos do objeto para as colunas corretas.
- Finalmente, salvará o workbook modificado com `workbook.save(output_path)`.

**Gerenciamento de Erros:**
- A falha na cópia inicial lançará uma `TemplateNotFoundError` (se o original não existir).
- Erros durante o preenchimento ou salvamento pelo openpyxl serão capturados e relançados como `TemplateFillError`.

## 7.0 Camada de Apresentação (GUI)

Esta seção descreve a interface gráfica do usuário (GUI), suas tecnologias, componentes e como ela interage com a camada de aplicação.

### 7.1 Tecnologia da Interface

- **Framework:** CustomTkinter
- **Justificativa:** CustomTkinter é uma biblioteca moderna baseada no Tkinter (padrão do Python), o que garante compatibilidade e leveza. Ela oferece widgets com aparência moderna e um sistema de temas (light/dark) de forma nativa, melhorando significativamente a experiência do usuário em comparação com o Tkinter padrão.

### 7.2 Padrão de Arquitetura da UI: Controller / ViewModel

Para manter a separação de responsabilidades, a UI seguirá um padrão similar ao MVC (Model-View-Controller):

- **View:** As classes que definem os widgets e a aparência visual da tela (o código CustomTkinter). Elas não contêm lógica de negócio.
- **Controller:** Uma classe que lida com os eventos da View (ex: cliques de botão). O Controller é responsável por chamar os Casos de Uso apropriados no Core e receber os resultados.
- **ViewModel (ou State Manager):** Um objeto que armazena o estado atual da UI (ex: caminhos de arquivos selecionados, listas de arquivos validados/não reconhecidos, etc.). O Controller atualiza o ViewModel, e a View se atualiza com base nos dados do ViewModel.

### 7.3 Estrutura da Janela Principal

A aplicação consistirá em uma única janela principal com uma estrutura de abas para guiar o usuário através do fluxo de trabalho.

**Janela Principal (MainWindow):**
- **Título:** "SAD App v2.0 - Sistema de Automação de Documentos"
- **Dimensões Mínimas:** 1280x720
- **Layout:**
  - **Topo:** Área para seleção de entradas principais.
  - **Centro:** Um notebook de abas (CTkTabbView).
  - **Fundo:** Uma área para o log em tempo real e uma barra de progresso.

### 7.4 Detalhamento das Abas e Componentes

**Área de Entrada Principal (Topo, sempre visível)**
- [Label] Manifesto de Entrada: [Entry (read-only)] [Botão "Selecionar..."]
- [Label] Pasta de Origem: [Entry (read-only)] [Botão "Selecionar..."]
- [Botão "VALIDAR LOTE"]: Inicia o UC-01. Fica desabilitado após o clique e durante o processamento.

**Aba 1: "Validação e Resolução"**

Esta aba é o painel de controle principal para as Fases 1 e 2.
- **Layout:** Dividida em duas colunas.

**Coluna Esquerda: "Arquivos Validados" (Frame)**
- [Label]: "Arquivos Validados (Total: 0)"
- [Treeview/ScrollableFrame]: Lista os arquivos que corresponderam ao manifesto. Colunas: Nome do Arquivo, Código do Documento.

**Coluna Direita: "Arquivos Não Reconhecidos" (Frame)**
- [Label]: "Arquivos Não Reconhecidos (Total: 0)"
- [Treeview/ScrollableFrame]: Lista os arquivos que não corresponderam. Permite seleção múltipla.

**Painel "Assistente de Resolução" (Frame - inicialmente desabilitado)**
- [Label]: "Resolver Arquivos Selecionados"
- [ComboBox]: Dropdown para selecionar o "Perfil de Extração" (RIR, etc.).
- [Botão "Tentar Resolver"]: Inicia o UC-02 para os arquivos selecionados.

**Aba 2: "Organização e Saída"**

Esta aba contém as configurações para a Fase 3 e o gatilho para a Fase 4. Ela só é habilitada após a conclusão bem-sucedida do UC-01.

**Painel "Configuração de Saída" (Frame)**
- [Label] Pasta de Destino: [Entry (read-only)] [Botão "Selecionar..."]
- [Label] Template Mestre: [Entry (read-only)] [Botão "Selecionar..."]
- [Label] Docs por Lote: [Entry (numérico)]
- [Label] Nº Sequencial Inicial: [Entry (numérico)]
- [Botão "ORGANIZAR E GERAR LOTES"]: Botão principal que inicia o UC-03. Fica desabilitado até que todos os campos de configuração sejam preenchidos.

**Área de Feedback (Fundo, sempre visível)**
- [Textbox (read-only)]: Log em tempo real.
- [ProgressBar]: Barra de progresso para operações longas.

### 7.5 Interação UI-Core (Mecanismo de Callback)

Para evitar que a lógica do Core dependa da UI (respeitando a Clean Architecture), a comunicação de progresso será feita via callbacks.

**Exemplo:** A chamada do Controller para o UC-03 será algo como:

```python
# Dentro de uma classe Controller
def on_organize_button_click(self):
    # ... obter parâmetros da UI ...
    progress_callback = self.view.update_log_and_progress # Passa um método da View

    # Inicia o caso de uso em uma thread separada para não congelar a UI
    thread = Thread(target=self.organize_use_case.execute, args=(params, progress_callback))
    thread.start()
```

O `OrganizeLotsUseCase` receberá esta função `progress_callback` e a chamará em pontos-chave (ex: `progress_callback("Balanceando lotes...", 20)`) para atualizar a UI sem conhecê-la diretamente.



