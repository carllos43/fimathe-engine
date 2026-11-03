# Fimathe – Motor Educacional e de Simulação

> **AVISO IMPORTANTE**  
> Este repositório é **exclusivamente educacional e de simulação**.  
> Não executa ordens reais, não se conecta a corretoras e **não promete nenhum resultado financeiro**.  
> A técnica Fimathe pertence a Marcelo Ferreira. Este projeto apenas documenta e modela as regras publicamente disponíveis de forma rastreável, para estudo e validação de lógica.  
> Trading envolve risco elevado de perda de capital. Use por sua conta e risco.

## Objetivo

Criar um motor determinístico que:
1. Representa fielmente as regras extraídas das fontes disponíveis.
2. Separa **fato confirmado** de **decisão de projeto** e de **lacuna**.
3. Permite simulação de candles sem execução real.
4. Facilita a validação visual contra os gráficos originais (quando os prints forem fornecidos).

## Status atual – v0.3 (pipeline v2)

**Motor matemático** + **orquestrador OHLC experimental** (funções puras + modelos tipados + testes).  
Ainda **sem** execução de ordens, **sem OCR de screenshot** e sem interface gráfica de trading.

| Variante / módulo | Fonte / papel | Status |
|-------------------|---------------|--------|
| Aula H1/M15 (pontos A/B) | Doc A | Regras catalogadas |
| Raiz / Zona Neutra | Transcrições | Geometria + testes |
| Teoria dos Ciclos | Transcrições + Doc B | Expansões plugáveis (C1–C4 provisional) |
| PCM | Doc B | Regras provisórias |
| Mapeamento superior + fatiamento | Transcrição 3 | Implementado (“Fimathe 350” math pending) |
| **Pipeline OHLC v2** | Pesquisa | `analyze_complete` + detector heurístico |
| Price Action (parcial) | Spec + código | swings / structure / confluence; LTA/candles ainda scaffold |
| Sessão (chat) | `docs/sessions/` | Continuidade manual via CURRENT.md |

### Pipeline v2 (experimental)

Entrada: **lista de candles OHLC** (não lê pixels de imagem).

| Função | Arquivo | O que faz |
|--------|---------|-----------|
| `analyze_complete` | `engine/analysis/complete_pipeline.py` | Orquestra validação OHLC → candidatos de canal → estado de fechamento/reteste → estrutura HH/HL/LH/LL → MTF opcional |
| `detect_channel_candidates` | `engine/channels/candidate_detector.py` | Envelopes heurísticos por pivôs (score ≠ probabilidade) |
| `classify_breakout` | `engine/price_action/breakouts.py` | Rompimento/reteste só com **candle fechado**; decisão sempre **WAIT** |
| `align_timeframes` | `engine/mapping/higher_tf.py` | Alinha viés HTF / meio / LTF; conflito → **WAIT** |

**Limites explícitos do v2**
- Não gera entrada, stop nem alvo operacional sem regra validada.
- Candidato de canal **não** é canal Fimathe oficial.
- Multi-TF exige séries já separadas por período (sem resampling automático).
- Imagem de gráfico continua dependendo de OCR/visão externa ou digitação de OHLC.

Documentação do patch: `IMPLEMENTACAO_COMPLETA_V2.md`, `IMPLEMENTACAO_PIPELINE_V1.md`, `PATCH_NOTES_V2.md`.

### Como rodar os testes

```bash
cd fimathe-engine   # ou o clone local
PYTHONPATH=. python -m pytest tests/unit -q
```

Esperado (após v2): dezenas de testes passando (inclui geometry, mapping, PA, pipeline completo).

### Continuidade de sessão (análise no chat)

Antes de redesenhar canal a cada print:
1. Ler `docs/SESSION_WORKFLOW.md`
2. Ler `docs/sessions/<ATIVO>/CURRENT.md`
3. Continuar o plano gravado; só reanalisar se `INVALIDADO` ou nova semana

### Documentação principal

- `docs/REGRAS_OPERACIONAIS.md` — teto operacional, entrada, stop, ZN
- `docs/SESSION_WORKFLOW.md` — fluxo profissional
- `docs/mathematical_engine.md` / `docs/fimathe_rules.md`
- `docs/PRICE_ACTION_ENGINE.md` — camada PA
- `docs/LACUNAS.md` — o que ainda falta
- `AGENTS.md` / `AI_CHART_WORKFLOW.md` — instruções para IAs

## Estrutura do repositório

```
fimathe-engine/
├── README.md
├── AGENTS.md
├── AI_CHART_WORKFLOW.md
├── IMPLEMENTACAO_COMPLETA_V2.md
├── docs/
├── rules/
├── engine/
│   ├── analysis/         # complete_pipeline, chart_pipeline, render
│   ├── channels/         # geometry, candidate_detector, visual_assessment
│   ├── breakouts/        # confirmation (B03)
│   ├── cycles/           # projections
│   ├── mapping/          # higher_tf, align_timeframes, fatiamento
│   ├── price_action/     # swings, structure, confluence, breakouts
│   └── core/             # models
├── tests/unit/
├── analysis/weekly/
├── examples/
└── data/
```

## Princípios

- Toda regra aponta para um ID e uma fonte quando possível.
- Nenhuma regra inventada como “oficial Fimathe” sem rastreio.
- Determinismo: mesma sequência de candles → mesmo resultado.
- Sem execução real de ordens.
- Preferir **AGUARDAR / WAIT** quando faltar confirmação.

## Licença e direitos

- Conteúdo educacional derivado de material público.
- **Não copie os PDFs originais** para dentro do repositório.
- Cite sempre a fonte e o autor (Marcelo Ferreira / Fimathe).
