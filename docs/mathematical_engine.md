# Motor matemático Fimathe – v0.2

## Visão geral

Pacote Python puro, determinístico, sem side-effects de mercado real.

```
engine/
├── core/models.py
├── channels/geometry.py
├── cycles/projections.py
├── breakouts/confirmation.py
├── mapping/higher_tf.py
└── analysis/ (chart_overlay, text_draw)
```

## Funções principais

### Geometria de canal
- `channel_amplitude(L, H)` → H − L
- `build_neutral_zone(ref, direction)` → NeutralChannel
- `level_50_of_channel(L, H)`
- `level_50_of_two_channels(...)`
- `project_levels(origin, amplitude, direction, multipliers)`

### Ciclos / expansões
- `create_expansion(...)` – nunca marca `confirmed_target=True` automaticamente
- `subcycle_from_entry(entry, amplitude, direction)`

### Rompimento
- `is_breakout_by_close(candle, channel, direction)` – só candle fechado

### Mapeamento e fatiamento
- `subdivide_interval(L, H, depth)` – metades sucessivas; nomenclatura “Fimathe 350” (math pending)
- `build_higher_tf_map(...)`
- `context_between_timeframes(...)`

### Overlay de gráfico puro
- `build_overlay(L, H, ...)` – pacote completo
- `analyze_and_draw(L, H, ...)` – desenho textual estilo gráfico

## Como rodar os testes

```bash
cd fimathe-engine
PYTHONPATH=. python -m pytest tests/unit -v
```

## Limitações (v0.2)

- Tendência de alta: zona neutra e subciclo são provisional
- Fórmula dos ciclos C1–C4 ainda plugável e desligada
- “Fimathe 350” registrado apenas como nomenclatura
- Canal de referência exige L/H explícitos (construção subjetiva)
