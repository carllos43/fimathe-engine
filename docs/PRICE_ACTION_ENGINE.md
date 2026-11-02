# PRICE_ACTION_ENGINE.md
## Especificacao de leitura de mercado e integracao com o Fimathe Engine

**Versao:** 1.0
**Tipo:** documentacao tecnica / especificacao funcional
**Objetivo:** adicionar uma camada de leitura de Price Action, estrutura de mercado e contexto de tendencia ao Fimathe Engine, sem substituir nem alterar silenciosamente as regras matematicas proprias da Fimathe.

> Arquivo completo disponivel no repositorio local e no historico da conversa.
> Implementacao: `engine/price_action/` | Testes: `tests/unit/test_price_action.py` | Resumo: `docs/PRICE_ACTION_README.md`

## 1. Objetivo do modulo

O modulo de Price Action transforma a leitura visual de um grafico em avaliacao estruturada, explicavel e verificavel. Funciona como camada de **contexto e confirmacao**. Nao sobrescreve calculos Fimathe.

## 2. Principios obrigatorios

- Separar: **Observado / Calculado / Inferido / Indisponivel**
- Nao inventar OHLC, entrada, stop, take, volume, timeframe
- Candle em formacao = provisorio; confirmacao so com fechamento
- Tendencia descreve estrutura observada, nao previsao
- Preservar Fimathe: nao alterar formulas; em divergencia, mostrar os dois resultados

## 3. Pipeline (resumo)

0. Qualidade da imagem (HIGH/MEDIUM/LOW)
1. Multi-timeframe (ou `higher_timeframe_status: unavailable`)
2. Regime: UPTREND / DOWNTREND / RANGE / TRANSITION / UNKNOWN
3. Estrutura HH/HL/LH/LL (pivos sem look-ahead)
4. BOS / CHoCH (rotulos descritivos)
5. LTA / LTB com pontuacao de qualidade
6. Canais de Price Action (distintos dos canais matematicos Fimathe)
7. Suporte / resistencia em zonas
8. Candles (padrao isolado nao gera ordem)
9. Volume / volatilidade (ou unavailable)
10. Rompimento / reteste / falha

## 4-6. Matriz de tendencia, integracao Fimathe, entrada/stop/take

Ver implementacao em `engine/price_action/confluence.py` e regras em `docs/REGRAS_OPERACIONAIS.md`.
Confluencia: ALIGNED / CONFLICTING / NEUTRAL / UNAVAILABLE.
Decisao: BUY_SETUP | SELL_SETUP | **WAIT**.

## 7-8. Contrato JSON e relatorio em 7 blocos

Relatorio no chat (obrigatorio):
1. Leitura do mercado
2. Estrutura
3. Linhas e regioes
4. Price Action
5. Leitura Fimathe
6. Plano operacional
7. Conclusao

Implementado em `engine/price_action/report.py` (`build_chat_report`).

## 9-12. Imagem, arquitetura, testes, aceitacao

Arquitetura: `engine/price_action/{models,swings,structure,trend,trendlines,channels,support_resistance,candlesticks,breakouts,volatility,confluence,report}.py`

Testes minimos: `tests/unit/test_price_action.py` (7 testes passando).

**Regra final:** se a leitura nao sustentar conclusao, a resposta e `WAIT — aguardando confirmacao`.

## 13-14. Fontes educacionais e aviso de escopo

Fontes CME, TradingView, PriceAction.com etc. sao referencia conceitual — **nao** regras oficiais Fimathe.
Modulo de analise e simulacao; nao e promessa de rentabilidade.
