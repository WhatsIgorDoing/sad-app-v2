# Unificação dos Botões de Ação na Interface

## Problema Original
Anteriormente, o botão "ORGANIZAR E GERAR LOTES" estava posicionado na parte inferior da aba de organização, ocupando um espaço significativo e ficando ocasionalmente coberto em modo tela cheia.

## Solução Implementada
Os botões principais de ação ("VALIDAR LOTE" e "ORGANIZAR E GERAR LOTES") foram unificados em uma única posição na interface, alternando dinamicamente com base na aba selecionada pelo usuário.

### Mudanças Realizadas

1. **Criação de um Frame Unificado para Botões**
   - Um novo frame `main_action_frame` foi adicionado abaixo das entradas de manifesto e pasta
   - Os dois botões principais compartilham o mesmo espaço, mas apenas um é visível por vez

2. **Sistema de Alternância Automática**
   - Implementado o método `_on_tab_changed` que é chamado quando o usuário muda de aba
   - Quando a aba "1. Validação e Resolução" está selecionada, o botão "VALIDAR LOTE" é mostrado
   - Quando a aba "2. Organização e Saída" está selecionada, o botão "ORGANIZAR E GERAR LOTES" é mostrado

3. **Feedback Visual para o Usuário**
   - Uma mensagem é adicionada ao log da aplicação informando o modo atual
   - O botão de organização mantém sua cor verde distintiva para diferenciá-lo do botão de validação

4. **Otimização do Layout**
   - O espaço antes ocupado pelo botão na aba de organização foi liberado
   - Melhorou o fluxo visual da interface, com o botão de ação sempre na mesma posição

## Benefícios

1. **Consistência de Interface**
   - O botão de ação principal está sempre no mesmo local, criando um padrão consistente
   - Reduz a curva de aprendizado para novos usuários

2. **Economia de Espaço**
   - Liberação de espaço na aba de organização, possibilitando adicionar mais controles no futuro se necessário
   - Menos elementos visuais competindo por atenção

3. **Melhor Visibilidade**
   - Elimina o problema do botão ser coberto em modo tela cheia
   - Posição mais proeminente na interface

4. **Fluxo de Trabalho Intuitivo**
   - A interface agora guia melhor o usuário através do processo de trabalho
   - Cada aba mostra apenas o botão relevante para aquela etapa

## Como Funciona

1. O usuário inicia a aplicação e vê o botão "VALIDAR LOTE" na primeira aba
2. Após validar, ao mudar para a segunda aba, o botão automaticamente muda para "ORGANIZAR E GERAR LOTES"
3. Se o usuário voltar para a primeira aba, o botão volta a ser "VALIDAR LOTE"