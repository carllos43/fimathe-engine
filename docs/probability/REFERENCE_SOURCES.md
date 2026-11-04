# Fontes de referência para Pattern Probability Engine

**Aviso:** estes links **não** são uma base de probabilidade Fimathe pronta.  
Servem para (1) obter **OHLC histórico** e (2) exemplos **visuais** de gráficos.  
Frequências tipo “58% alta” só são válidas depois de extrair features, definir outcome e contar casos com amostra e intervalo de incerteza.

Projeção matemática Fimathe ≠ probabilidade estatística. Manter separado no relatório.

---

## 1. OHLC histórico (prioridade para probabilidade real)

Sem série OHLC não há frequência confiável — só impressão visual.

| Fonte | Link | O que oferece |
|-------|------|----------------|
| **getdata-finance EURUSD 1m (sample GitHub)** | https://github.com/getdata-finance/eurusd-1m-ohlcv-forex-historical-data | CSV 1m sample (~187k–189k candles); ideal para protótipo M15 (agregar) |
| **GitHub Pages / preview** | https://getdata-finance.github.io/eurusd-1m-ohlcv-forex-historical-data/ | Visualização do sample |
| **Dataset completo (site)** | https://getdata.finance/datasets/eurusd | 11 timeframes (1m…1W), arquivo maior |
| **ejtraderLabs historical-data** | https://github.com/ejtraderLabs/historical-data | EURUSD m15/m30/h1/h4/d1 ~10 anos via raw.githubusercontent |
| **philipperemy FX-1-Minute-Data** | https://github.com/philipperemy/FX-1-Minute-Data | Histórico 1m multi-pares (HistData); útil para bulk |
| **Dukascopy downloader** | https://github.com/theorycraft-trading/dukascopy | Tool para baixar ticks/barras (não é dataset estático) |
| **FX-Data EURUSD-DS** | https://github.com/FX-Data/FX-Data-EURUSD-DS | Histórico por ano (branches) |

**Uso no motor:** carregar CSV → agregar para M15/H1 → extrair features (R = (P−L)/(H−L), pivôs, amplitude) → buscar vizinhos → outcomes → frequência + n + incerteza.

---

## 2. Imagens / charts educacionais (referência visual)

Úteis para anotar casos à mão e calibrar “o que parece semelhante”. **Não** substituem OHLC.

| Fonte | Link | Nota |
|-------|------|------|
| **Wikimedia EURUSD candlestick** | https://commons.wikimedia.org/wiki/File:Candlestick-chart.png | Imagem pública simples |
| **DollarContext case study EURUSD** | https://www.dollarcontext.com/cs0025-eurusd/ | Padrões de candle anotados (educacional) |
| **Brooks Trading Course EURUSD** | https://www.brookstradingcourse.com/analysis/eurusd-overlapping-candlesticks/ | Estrutura mensal/semanal (Price Action educacional) |
| **TradingView EURUSD ideas** | https://www.tradingview.com/symbols/EURUSD/ | Ideias públicas (canais, triângulos, estrutura) |
| **TradingView canal breakout exemplo** | https://www.tradingview.com/chart/EURUSD/HnGq6kHJ-EUR-USD-Channel-Breakout-Pattern/ | Exemplo de canal + rompimento (não oficial Fimathe) |
| **TradingView estrutura HH/HL** | https://www.tradingview.com/chart/EURUSD/uIUjk2Uc-EUR-USD-DAILY-CHART-MARKET-STRUCTURE-TREND-ANALYSIS/ | Template educacional de estrutura |
| **ColibriTrader EURUSD historical analysis** | https://www.colibritrader.com/most-detailed-eurusd-historical-analysis | Análise diária longa |
| **Investing.com EURUSD candlestick** | https://www.investing.com/currencies/eur-usd-candlestick | Charts + lista de padrões |

---

## 3. Como alimentar o módulo de probabilidade

1. Baixar OHLC (seção 1), preferir M15/H1 alinhados à operação.
2. Para cada janela histórica: calcular features Fimathe (amplitude, R, toques, bias).
3. Definir **outcome** fixo: ex. “atingiu T1 antes do stop em N candles”.
4. Buscar k vizinhos por distância de features (não por “parece o mesmo print”).
5. Reportar: n, frequência, intervalo (ex. Wilson), qualidade da match — **nunca** só “58%”.
6. Imagens da seção 2: só para **anotar** casos de ouro humanos, não para contagem automática.

---

## 4. Pastas sugeridas

```text
data/references/     # índice + links
data/ohlc/           # CSVs baixados (git-ignore se grandes)
docs/probability/REFERENCE_SOURCES.md
```

## 5. Sessão EURUSD

Sessão de venda com stop **1.12175** foi **INVALIDADA** (preço ~1.12559).  
O módulo de probabilidade, quando existir, pode estudar quantas vezes em condições semelhantes o preço continuou alta vs reverteu — isso exige OHLC histórico, não o print isolado.
