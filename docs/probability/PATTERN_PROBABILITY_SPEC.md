# Pattern Probability Engine — spec (v0 experimental)

Camada de **pesquisa**, independente do detector de canal oficial Fimathe.

## O que existe

| Módulo | Função |
|--------|--------|
| `engine/patterns/features.py` | `extract_features` → `ScenarioFeatures` normalizados |
| `engine/patterns/similarity.py` | distância / score / `rank_neighbors` |
| `engine/patterns/historical_search.py` | busca por similaridade |
| `engine/patterns/pattern_store.py` | store em memória de padrões rotulados |
| `engine/probability/outcomes.py` | `classify_outcome` (up_first / down_first / lateral) |
| `engine/probability/estimator.py` | frequências + disclaimer |
| `engine/probability/confidence.py` | Wilson interval + qualidade da amostra |
| `engine/analysis/probability_report.py` | relatório features + histórico (se houver store) |

## O que não existe (ainda)

- Loader de CSV OHLC
- Calibração out-of-sample
- Entrada/stop automáticos a partir de frequência
- Base histórica pré-carregada no repo

## Fontes de dados

Ver `docs/probability/REFERENCE_SOURCES.md`.

## Princípio

Frequência histórica **descreve o passado dos vizinhos**.  
Não substitui confirmação Fimathe (fechamento, ZN, stop).  
Amostra pequena → `quality: very_low` e intervalo largo.
