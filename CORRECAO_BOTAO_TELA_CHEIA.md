# Correção do Botão "ORGANIZAR E GERAR LOTES" em Modo Tela Cheia

## Problema
Quando a aplicação é executada em modo tela cheia, o botão "ORGANIZAR E GERAR LOTES" na aba de organização estava sendo coberto por outros elementos da interface, tornando-o inacessível para o usuário.

## Solução Implementada
As seguintes modificações foram realizadas no arquivo `src/sad_app_v2/presentation/main_view.py` para corrigir o problema:

1. **Adição de espaço flexível após os controles**
   ```python
   tab.grid_rowconfigure(6, weight=1)  # Adiciona espaço flexível após os controles
   ```
   
   Esta linha adiciona um espaçamento flexível que permite que o layout se ajuste adequadamente quando a janela é redimensionada em modo tela cheia.

2. **Adição de um frame espaçador**
   ```python
   spacer = ctk.CTkFrame(tab, height=1, fg_color="transparent")
   spacer.grid(row=5, column=0, columnspan=3, sticky="ew")
   ```
   
   Este espaçador transparente ajuda a garantir que exista um espaço entre os controles acima e o botão principal.

3. **Reposicionamento do botão em um frame separado**
   O botão foi movido para um frame dedicado, que é posicionado na linha 6 com espaçamento vertical adicional:
   
   ```python
   button_frame = ctk.CTkFrame(tab)
   button_frame.grid(
       row=6,
       column=0,
       columnspan=3,
       padx=10,
       pady=(20, 40),  # Espaçamento maior no topo e na base
       sticky="ew"
   )
   ```

4. **Aumento do tamanho do botão**
   ```python
   self.organize_button = ctk.CTkButton(
       button_frame, text="ORGANIZAR E GERAR LOTES", height=50, fg_color="green"
   )
   ```
   
   O botão foi aumentado de altura de 40 para 50 pixels para melhorar a visibilidade.

## Como a Solução Funciona
Estas mudanças garantem que o botão:
- Esteja sempre visível, mesmo em modo tela cheia
- Tenha espaço adequado acima e abaixo para evitar sobreposições
- Seja colocado em um contêiner dedicado que mantém sua posição e visibilidade
- Tenha tamanho aumentado para melhor visibilidade e usabilidade

## Teste da Solução
Para testar se a correção foi aplicada com sucesso:

1. Execute a aplicação
2. Alterne para o modo tela cheia
3. Navegue até a aba de organização
4. Verifique se o botão "ORGANIZAR E GERAR LOTES" está completamente visível e clicável