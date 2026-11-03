# Pipeline integrado v2 (experimental)

## Implementado
- `engine/analysis/complete_pipeline.py`: valida OHLC, executa detector de candidatos, escolhe candidato heurístico superior, estima estado de fechamento/rompimento/reteste, classifica swings HH/HL/LH/LL e compara três períodos quando OHLC superior/intermediário são fornecidos.
- Entrada e stop permanecem `not_generated`; canal candidato, rompimento e reteste não são por si só gatilho de operação.
- Candle aberto retorna estado pendente; somente candle fechado pode gerar rótulo de fechamento fora do candidato.
- Testes para contrato de saída, OHLC não finito e candle aberto.

## Limitações explícitas
- Não há OCR/visão computacional para transformar pixels do screenshot em OHLC. Essa camada precisa fornecer candles.
- Detector, seleção, reteste e estrutura são heurísticos, não regras oficiais Fimathe nem probabilidade de sucesso.
- Multi-timeframe usa candles já separados por período; não faz resampling automático nem valida alinhamento temporal.
- Não produz preço de entrada, stop ou alvo operacional sem regra específica validada.

## Teste
Execute da raiz do projeto: `PYTHONPATH=. pytest -q`
