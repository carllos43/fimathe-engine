# Instruções obrigatórias para agentes de IA

Ao receber um print de gráfico de trading neste repositório, siga `AI_CHART_WORKFLOW.md`.

Em resumo:
- Leia as regras e exemplos Fimathe do repositório antes de analisar.
- Interprete o print por conta própria; não exija que o usuário desenhe o canal.
- Identifique swings/pontos A-B e selecione o canal conforme regras documentadas.
- Verifique rompimento pelo fechamento quando a regra assim exigir.
- Calcule entrada, stop, zona neutra, 50% e takes somente conforme as regras/variantes.
- Desenhe os candles diretamente na resposta usando ASCII/Unicode, visualmente semelhante ao
  print, com pavios, corpos, escala de preço e linhas de níveis. Não gere imagem separada, salvo
  pedido explícito do usuário.
- Diferencie observações visuais, estimativas, regras confirmadas e hipóteses.
- Não invente precisão de OHLC nem afirme que uma operação foi confirmada se o print não permitir.

## Price Action + relatório

Ao analisar prints, use também `docs/PRICE_ACTION_ENGINE.md` e `engine/price_action/`.
Responda no formato de **7 blocos** definido em `docs/PRICE_ACTION_ENGINE.md` (seção 8) e
em `docs/REGRAS_OPERACIONAIS.md` para canal Fimathe (teto canal+ZN ≤ 0,00350 em preço).
Decisão final: COMPRA / VENDA / **AGUARDAR**. Sem confirmação → AGUARDAR.
