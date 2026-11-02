# Price Action Layer

Especificação completa: [`PRICE_ACTION_ENGINE.md`](./PRICE_ACTION_ENGINE.md)

Implementação inicial: `engine/price_action/`

- `models.py` — enums e dataclasses do contrato
- `swings.py` — pivôs sem look-ahead
- `structure.py` — HH/HL/LH/LL
- `trend.py` — regime de mercado
- `confluence.py` — cruzamento com Fimathe (não sobrescreve geometria)
- `report.py` — relatório em 7 blocos para o chat
- Demais arquivos (`trendlines`, `channels`, …) — scaffold

Regras operacionais Fimathe: [`REGRAS_OPERACIONAIS.md`](./REGRAS_OPERACIONAIS.md)

Testes: `tests/unit/test_price_action.py`
