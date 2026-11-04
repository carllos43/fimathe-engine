# Regras operacionais Fimathe — consolidadas

Documento prático derivado do repositório (`docs/visual_channel_localization.md`,
`rules/visual_channel_localization.yaml`, `docs/fimathe_rules.md`, geometria do motor)
e das decisões operacionais validadas na aplicação dos prints (exemplos em EURUSD/XAUUSD, regras válidas para **qualquer ativo**).

Status: **operacional / em uso**. Onde houver conflito com regra ainda provisional do motor,
este documento deixa a pendência explícita.

**Escopo:** estas regras operacionais valem para **todos os ativos** (Forex, índices, ações, cripto, commodities) e timeframes. O exemplo em EURUSD/XAUUSD é apenas ilustrativo.

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

Esta regra de teto é **operacional** e vale como referência para **FX**. Em ativos com cotação muito diferente (ex.: ouro), priorizar amplitude da região onde o preço bateu e voltou; manter simetria canal + ZN.

---

## 3. Geometria (motor)

| Item | Fórmula / regra | Status |
|------|-----------------|--------|
| Amplitude | `H − L` | Confirmado |
| 50% do canal | `(L + H) / 2` | Confirmado |
| ZN em tendência de **baixa** / setup de **venda** | `H` até `H + amplitude` (**acima** do canal) | Confirmado (operacional) |
| ZN em tendência de **alta** / setup de **compra** | `L − amplitude` até `L` (**abaixo** do canal) | Confirmado (operacional) |
| Stop | Além do limite externo da Zona Neutra | Confirmado (buffer exato não especificado) |
| Rompimento | Só com **fechamento** de vela fora do canal; sombra não conta | Confirmado (B03) |
| Alvos/projeções | Nunca marcar automaticamente como alvo oficial | Confirmado |

### 3.1 Zona Neutra — regra operacional (todos os ativos)

Regra registrada para o motor e para análises no chat:

| Direção do setup | Onde fica a Zona Neutra | Stop de referência |
|------------------|-------------------------|---------------------|
| **Compra** (bias de alta) | **Abaixo** do canal: de `L − amplitude` até `L` | Além da base da ZN (mais baixo que `L − amplitude`) |
| **Venda** (bias de baixa) | **Acima** do canal: de `H` até `H + amplitude` | Além do topo da ZN (mais alto que `H + amplitude`) |

- A ZN **copia a amplitude** do canal de referência (`amplitude = H − L`).
- Preço de compra opera **acima** da ZN; preço de venda opera **abaixo** da ZN.
- Não inverter ZN de compra com ZN de venda.
- Em ativos com cotação muito diferente do FX (ex.: ouro ~4000), o teto `0,00350` em preço absoluto do §2 pode ser impraticável; priorizar canal na região onde o preço bateu e voltou e manter a **simetria** canal + ZN (mesma amplitude), sem inflar o pacote.

Implementação: `engine/channels/geometry.py` (`build_neutral_zone`), `engine/breakouts/confirmation.py`.

---

## 4. Quando há operação

### 4.1 Venda (bias de baixa)

- Entrada **somente** se a vela do timeframe **fechar abaixo do L** do canal.
- Entrada hipotética: ligeiramente além do L.
- Stop: limite externo da ZN (topo da ZN em baixa).
- Enquanto o preço estiver **dentro** do canal → **sem operação**.

### 4.2 Compra (bias de alta)

- ZN **abaixo** do L (ver §3.1).
- Preferir confirmação por **fechamento** e estrutura de alta.
- Stop: além da base da ZN.
- Não comprar no extremo do impulso sem canal operacional claro.

### 4.3 O que não é entrada

- Sombra fora do canal sem fechamento.
- Canal candidato sem revisão das regras VCL.
- Frequência histórica do módulo de probabilidade (não é gatilho).

---

## 5. Continuidade de sessão

Ver `docs/SESSION_WORKFLOW.md` e `docs/sessions/<ATIVO>/CURRENT.md`.
Não redesenhar o canal a cada print se o plano ainda é válido.
