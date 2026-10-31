# Regras operacionais Fimathe — consolidadas

Documento prático derivado do repositório (`docs/visual_channel_localization.md`,
`rules/visual_channel_localization.yaml`, `docs/fimathe_rules.md`, geometria do motor)
e das decisões operacionais validadas na aplicação dos prints (exemplos em EURUSD, regras válidas para **qualquer ativo**).

Status: **operacional / em uso**. Onde houver conflito com regra ainda provisional do motor,
este documento deixa a pendência explícita.

**Escopo:** estas regras operacionais valem para **todos os ativos** (Forex, índices, ações, cripto, commodities) e timeframes. O exemplo em EURUSD é apenas ilustrativo.

---

## 1. Localização do Canal de Referência

1. Declarar a **tendência / bias** antes de marcar o canal.
2. Localizar o canal **onde o preço está** — região atual de negociação.
3. Pontos A/B = **suporte e resistência com relevância**: onde o preço **bateu e voltou**.
4. Justificar cada lado com evidência visual (topo, fundo, consolidação).
5. A marcação pode usar **corpo ou sombra**, conforme o tamanho pretendido do canal.
6. Evitar canal **estreito demais** (entrada precoce/errada) e **largo demais** (atrasa entrada / stop inviável).
7. Não existe número fixo de toques obrigatório.
8. O canal marcado é **candidato visual**, não confirmação oficial automática da técnica.

Referências: `docs/visual_channel_localization.md`, regras VCL01–VCL12.

---

## 2. Tamanho máximo do pacote (regra prática)

| Regra | Valor |
|-------|-------|
| **Canal + Zona Neutra** | **≤ 0,00350** em preço (ex.: 35 pips no EURUSD; em outros ativos usar a mesma distância em preço) |
| Amplitude máxima do canal | **≤ 0,00175** em preço, porque a ZN copia a amplitude |

Se o pacote canal + ZN estourar 0,00350:

- o stop fica caro demais;
- o setup tende a perder o movimento da janela analisada;
- deve-se **apertar** o canal usando a região atual e, se preciso, marcação por **corpo**.

Esta regra de teto é **operacional** e vale para **todos os ativos** (FX, índices, cripto, etc.).
O número 0,00350 é distância em **preço**, não um conceito exclusivo do EURUSD.
Em pares com outra cotação, manter a mesma lógica de teto; o equivalente em pips/points muda por símbolo.
O material de origem alerta qualitativamente contra canal largo/estreito, sem fixar o número 0,00350.

---

## 3. Geometria (motor)

| Item | Fórmula / regra | Status |
|------|-----------------|--------|
| Amplitude | `H − L` | Confirmado |
| 50% do canal | `(L + H) / 2` | Confirmado |
| ZN em tendência de **baixa** | `H` até `H + amplitude` | Confirmado |
| ZN em tendência de **alta** | `L − amplitude` até `L` | **Provisional** |
| Stop | Além do limite externo da Zona Neutra | Confirmado (buffer exato não especificado) |
| Rompimento | Só com **fechamento** de vela fora do canal; sombra não conta | Confirmado (B03) |
| Alvos/projeções | Nunca marcar automaticamente como alvo oficial | Confirmado |

Implementação: `engine/channels/geometry.py`, `engine/breakouts/confirmation.py`.

---

## 4. Quando há operação

### 4.1 Venda (bias de baixa)

- Entrada **somente** se a vela do timeframe **fechar abaixo do L** do canal.
- Entrada hipotética: ligeiramente além do L.
- Stop: limite externo da ZN (topo da ZN em baixa).
- Enquanto o preço estiver **dentro** do canal → **sem operação**.

### 4.2 Compra (exemplo de alta do material de origem)

- Após **retorno** do preço e **rompimento do 50%** do Canal de Referência para cima.
- Confirmação por **fechamento**.
- Não generalizar esse exemplo para todos os cenários sem apoio da documentação.

### 4.3 O que não é entrada

- Estar apenas abaixo ou acima do 50%.
- Pavio/sombra atravessar L ou H sem fechamento fora.
- “Parecer fraco” ou “parecer forte” sem condição de rompimento confirmada.

---

## 5. Checklist antes de marcar no gráfico

1. Onde o preço está batendo **agora**?
2. Qual suporte relevante (bateu e voltou)? → **L**
3. Qual resistência relevante (bateu e voltou)? → **H**
4. `H − L` ≤ **0,00175**?
5. Canal + ZN ≤ **0,00350**?
6. Tendência/bias declarado?
7. Entrada só com **fechamento** fora do canal?
8. Stop além da ZN?

Se 4 ou 5 falharem: apertar A/B na região atual (preferir corpos se a sombra deixar o canal largo).

---

## 6. Exemplo consolidado (EURUSD M15 — apenas ilustração)

As regras das seções 1–5 e 7–9 valem para **qualquer ativo e timeframe**.
O exemplo abaixo é só uma aplicação numérica em EURUSD após confirmação do suporte e do teto 0,00350:

| Nível | Preço | Motivo |
|-------|-------|--------|
| **L** | **1.11400** | Suporte onde o preço bateu e voltou |
| **H** | **1.11575** | `L + 0,00175` (respeita teto canal+ZN) |
| **50%** | **1.114875** | `(L + H) / 2` |
| **ZN** | **1.11575 – 1.11750** | Colada acima do canal (bias baixa) |
| **STOP** | **1.11750** | Além da ZN |
| Amplitude | 0,00175 (17,5 pips) | |
| Canal + ZN | 0,00350 (35 pips) | No teto operacional |

```
1.11750 ── STOP / topo ZN
1.11575 ══ H / fundo ZN
1.11488 ┄  50%
1.11400 ══ L suporte
```

- Preço ~1.11584 na borda superior do canal / início da ZN.
- Venda só com fechamento **abaixo de 1.11400**.
- O nível 1.12000 pode permanecer como **resistência de contexto**, mas não como H deste canal operacional (estouraria o teto).

---

## 7. Prioridade de fontes

1. Regras confirmadas e exemplos rotulados no repositório.
2. Implementação e testes do motor.
3. Regras provisórias (sempre explicitadas).
4. Heurísticas visuais e tetos operacionais deste documento — declarados como tal.

---

## 8. Política de resposta / integridade

- Separar sempre: **estimado / pendente / confirmado**.
- Não inventar OHLC exato quando a escala do print não permitir.
- Não transformar projeção matemática em alvo garantido.
- Não afirmar rompimento sem fechamento verificável.
- Análise educacional e de simulação — não envia ordens.

---

## 9. Relação com outros arquivos

| Arquivo | Papel |
|---------|-------|
| `docs/visual_channel_localization.md` | Procedimento visual A/B |
| `rules/visual_channel_localization.yaml` | Regras VCL estruturadas |
| `docs/fimathe_rules.md` | Regras matemáticas extraídas |
| `docs/image_analysis_contract.md` | Contrato imagem → motor → chat |
| `AI_CHART_WORKFLOW.md` | Fluxo da IA ao receber print |
| `engine/channels/geometry.py` | Amplitude, 50%, ZN |
| `engine/breakouts/confirmation.py` | Rompimento por fechamento |

---

*Última consolidação: regras universais (qualquer ativo) + teto operacional canal+ZN ≤ 0,00350 em preço + exemplo ilustrativo EURUSD 1.11400.*
