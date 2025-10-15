# Adição do botão "Selecionar Todos" para arquivos não reconhecidos

## Problema
Quando há muitos arquivos não reconhecidos na interface, o usuário precisava selecionar manualmente cada um deles para poder processá-los, o que era tedioso e demorado.

## Solução Implementada
Foi adicionado um conjunto de botões "Selecionar Todos" e "Desmarcar Todos" na parte superior da lista de arquivos não reconhecidos. 

### Funcionalidades
- Botão "Selecionar Todos": Marca todos os checkboxes de arquivos não reconhecidos com um único clique
- Botão "Desmarcar Todos": Desmarca todos os checkboxes de arquivos não reconhecidos com um único clique

### Detalhes Técnicos
1. Os botões são criados dentro de um frame transparente no topo da lista de arquivos não reconhecidos
2. Quando clicados, os botões chamam os métodos `_select_all_checkboxes` ou `_deselect_all_checkboxes`
3. Após selecionar ou desmarcar todos os checkboxes, o controlador é notificado para atualizar o estado dos botões de ação

## Benefícios
- Economiza tempo do usuário
- Melhora a experiência de uso
- Facilita a seleção de múltiplos arquivos para processamento em lote
- Garante que todos os arquivos sejam processados sem omissão acidental

## Como Usar
1. Ao validar um lote, se houver arquivos não reconhecidos, os botões aparecerão automaticamente
2. Clique em "Selecionar Todos" para marcar todos os arquivos
3. Clique em "Desmarcar Todos" para desmarcar todos os arquivos
4. Após selecionar os arquivos desejados, utilize as funcionalidades de processamento normalmente