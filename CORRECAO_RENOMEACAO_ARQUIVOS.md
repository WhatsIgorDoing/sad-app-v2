# Correção do Problema de Arquivos Renomeados

## Problema
Após renomear arquivos não reconhecidos para o formato correto, o sistema não estava conseguindo encontrar os arquivos com os novos nomes ao tentar gerar a saída final. O sistema apresentava erro como se o arquivo não fosse encontrado no caminho atualizado, continuando a usar a referência ao nome anterior.

## Causa Raiz
1. **Inconsistência nas Referências**: Ao renomear os arquivos durante o processo de resolução RIR (Reconhecimento Inteligente de Relatórios), o sistema criava novos objetos `DocumentFile` com os caminhos atualizados, mas havia inconsistências no uso dos atributos `manifest_item` e `associated_manifest_item`.

2. **Falta de Validação**: O sistema não verificava se os arquivos existiam fisicamente nos caminhos referenciados antes de tentar organizá-los nos lotes de saída.

3. **Ambiguidade de Nomenclatura**: O código utilizava dois nomes diferentes para o mesmo conceito (`manifest_item` e `associated_manifest_item`), causando confusão e inconsistência nos dados.

## Solução Implementada

### 1. Adição de Validação de Existência de Arquivos
Adicionamos uma verificação inicial no método `execute` do caso de uso `OrganizeAndGenerateLotsUseCase` para identificar arquivos que não existem fisicamente nos caminhos referenciados:

```python
# Validação inicial - verificar se os arquivos existem
nonexistent_files = []
for file in validated_files:
    if not file.path.exists():
        nonexistent_files.append(file)

if nonexistent_files:
    error_msg = "Alguns arquivos não foram encontrados nos caminhos esperados:\n"
    # Gera mensagem detalhada de erro
    raise CoreError(error_msg)
```

### 2. Compatibilidade entre Campos
Implementamos property getters e setters na classe `DocumentFile` para garantir consistência entre `manifest_item` e `associated_manifest_item`:

```python
@property
def manifest_item(self):
    """Getter para manter compatibilidade com código legado."""
    return self.associated_manifest_item

@manifest_item.setter
def manifest_item(self, value):
    """Setter que atualiza ambos os campos para manter compatibilidade."""
    self.associated_manifest_item = value
    self._manifest_item = value
```

### 3. Atualização do Processo de Renomeação
Atualizamos o método de resolução RIR para definir ambos os atributos:

```python
resolved_file = DocumentFile(new_path, file.size_bytes)
if matched_item:
    resolved_file.manifest_item = matched_item
    resolved_file.associated_manifest_item = matched_item  # Adicionado para compatibilidade
```

## Impacto da Solução
1. **Mensagens de Erro Claras**: Quando um arquivo não é encontrado, o sistema agora apresenta uma mensagem de erro clara com detalhes sobre quais arquivos estão faltando.

2. **Consistência de Dados**: O sistema agora mantém os dados consistentes entre as diferentes partes do código, independentemente de qual atributo é usado para referência.

3. **Prevenção de Falhas Silenciosas**: A validação inicial previne que o sistema tente processar arquivos inexistentes, evitando erros em estágios posteriores do processo.

## Como Verificar
Após esta correção, o sistema deve:
1. Reconhecer corretamente arquivos que foram renomeados
2. Encontrar os arquivos em seus novos caminhos ao gerar os lotes de saída
3. Apresentar mensagens de erro mais claras caso algum arquivo esteja faltando