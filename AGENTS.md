# Instruções obrigatórias para agentes de IA

Ao receber um print de gráfico de trading neste repositório, siga `AI_CHART_WORKFLOW.md`.

Em resumo:
- Leia as regras e exemplos Fimathe do repositório antes de analisar.
- Interprete o print por conta própria; não exija que o usuário desenhe o canal.
- Identifique swings/pontos A-B e selecione o canal conforme regras documentadas.
- Verifique rompimento pelo fechamento quando a regra assim exigir.
- Calcule entrada, stop, zona neutra, 50% e takes somente conforme as regras/variantes.
- Desenhe os candles diretamente na resposta usando ASCII/Unicode.
- Diferencie observações visuais, estimativas, regras confirmadas e hipóteses.
- Não invente precisão de OHLC nem afirme operação confirmada sem base no print.

## Price Action + relatório

Use `docs/PRICE_ACTION_ENGINE.md` e `engine/price_action/`.
Responda no formato de **7 blocos**. Decisão: COMPRA / VENDA / **AGUARDAR**.

## Continuidade de sessão (obrigatório)

Antes de analisar qualquer print:
1. Ler `docs/SESSION_WORKFLOW.md`.
2. Ler `docs/sessions/<ATIVO>/CURRENT.md` se existir.
3. **Continuar** o canal/bias/plano gravado — não redesenhar do zero.
4. Atualizar `CURRENT.md` + `log.md` após a checagem.
5. Análise semanal (domingo/segunda) em `analysis/weekly/`.
6. Só reanalisar por completo se status `INVALIDADO` ou nova semana.
