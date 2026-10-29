# Regras Fimathe extraídas das transcrições

Separação rigorosa entre fato, interpretação e pendência.

## 1. Regras explicitamente descritas (alto grau de confiança)

| ID | Regra | Fonte |
|----|-------|-------|
| R_amplitude | amplitude = H − L | Transcrição motor |
| B_neutral_down | Em tendência de baixa: neutral_lower = H; neutral_upper = H + amplitude | Transcrição motor + 2ª |
| B03 | Rompimento só vale com **fechamento** de vela fora do canal; sombra não conta | Transcrição motor + Doc B |
| B_stop_beyond | Stop posicionado além do limite externo da zona neutra | 2ª transcrição |
| R_50 | Nível de 50% de um canal = (L + H) / 2 | Transcrição + Doc A |
| R_no_auto_target | Nenhuma expansão é escolhida automaticamente como alvo confirmado | Transcrição 3 |
| R_no_future | Não usar candles futuros nem tratar candles abertos como fechados | Transcrição 3 |

## 2. Interpretações matemáticas necessárias à implementação

| Interpretação | Status | Observação |
|---------------|--------|------------|
| Zona neutra em tendência de alta = simétrica (L − amplitude, L) | **Provisional** | Fonte só exemplificou baixa |
| cycle_height = 2 × amplitude | Interpretação do exemplo | Pode ser só o caso ilustrado |
| subciclo = entry − amplitude (baixa) | Interpretação do exemplo | |
| Fatiamento = subdivisão sucessiva em metades (2^depth partes) | Interpretação de “Fimathe 350” | Correspondência matemática exata **pendente** |
| Projeções com multiplicadores 1 / 1.5 / 2 | Configurável | Origem de medição ainda não confirmada visualmente |

## 3. Hipóteses ainda não confirmadas / regras pendentes

- Qual dos dois níveis de 50% prevalece em cada contexto
- Critérios completos de reversão para tendência de alta
- Origem exata da “projeção de dois níveis”
- Relação matemática definitiva entre CA/C1/C2/C3/C4 e os alvos T1/T2
- Simetria completa das regras para alta e baixa
- Construção objetiva do Canal de Referência / pontos A-B (continua subjetiva)
- Significado matemático preciso da nomenclatura **“Fimathe 350”**

## 4. Política do motor

- Toda função pura devolve `CalculationResult` com `rule_id`, `rule_version`, `clarity` e `warnings`.
- Regras provisional/unverified nunca são apresentadas como oficiais pela camada de explicação.
- O usuário pode sempre sobrescrever limites de canal (construção subjetiva).
