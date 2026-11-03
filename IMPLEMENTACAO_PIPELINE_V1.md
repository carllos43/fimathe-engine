# Implementação local — pipeline de análise v1

Esta entrega acrescenta uma primeira camada executável de pesquisa:

- `detect_channel_candidates`: pivôs confirmados (left/right), envelopes candidatos, contagem de toques e score heurístico transparente.
- `classify_breakout`: classificação baseada apenas em candles fechados, tentativa/rompimento e observação de reteste. A saída continua `WAIT`; não inventa entrada.
- `align_timeframes`: separa viés superior, estrutura intermediária e gatilho inferior; conflito ou falta de dados não cria operação.
- testes unitários para dados inválidos, candles abertos, rompimento e conflito MTF.

## Limites importantes

O detector é experimental: canal candidato não significa canal Fimathe oficial. A seleção de pivôs e score não foram calibrados com exemplos oficiais nem com validação histórica. O reteste é uma regra heurística inicial e ainda precisa ser refinado conforme a definição de Price Action/Fimathe que o usuário confirmar. A função MTF recebe as classificações de cada timeframe; não calcula tendência/estrutura automaticamente a partir de três séries.

Não usar como recomendação financeira nem como sinal automatizado. Próxima etapa: integrar OHLC extraído de imagem com o detector, apresentar alternativas e evidências, e validar contra charts anotados antes de automatizar a escolha.

Testes: `python -m pytest tests/unit -q`.
