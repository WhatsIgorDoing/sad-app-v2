# Simplificação da Interface de Resolução de Arquivos

## Mudança Implementada
O sistema foi simplificado para mostrar apenas a opção "RIR (buscar nome no documento)" na interface de resolução de arquivos não reconhecidos. Esta mudança foi feita para melhorar a experiência do usuário, removendo opções que não estavam sendo usadas efetivamente no processo de resolução.

## Arquivos Modificados

### 1. `src/sad_app_v2/main.py`
- Removida a criação desnecessária da lista de perfis `["PID", "GERAL"]`
- Atualizado o comentário para esclarecer que apenas a opção RIR é utilizada
- A chamada para `populate_profiles_dropdown` agora recebe uma lista vazia, indicando claramente que os perfis passados são ignorados

### 2. `src/sad_app_v2/presentation/main_view.py`
- Adicionada documentação detalhada ao método `populate_profiles_dropdown`
- Esclarecido que o método mantém apenas a opção RIR, independentemente dos perfis passados como parâmetro

## Benefícios
1. **Simplificação da Interface**: O usuário agora vê apenas a opção que realmente funciona e é utilizada pelo sistema
2. **Redução de Confusão**: Elimina a possibilidade de selecionar opções que não têm implementação completa
3. **Código Mais Claro**: A documentação e implementação agora refletem com precisão o comportamento real do sistema
4. **Manutenção Simplificada**: Menor chance de bugs relacionados à seleção de perfis não implementados

## Comportamento Atual
Quando o usuário seleciona arquivos não reconhecidos e clica em "Tentar Resolver Selecionados", o sistema aplica automaticamente o algoritmo RIR (Reconhecimento Inteligente de Relatórios), que:
1. Extrai texto do documento
2. Busca o nome após "Relatório:" no texto extraído
3. Procura correspondências no manifesto
4. Renomeia o arquivo baseado no nome extraído e na revisão encontrada

Esta abordagem foca nas capacidades reais do sistema, garantindo uma experiência mais previsível para o usuário.