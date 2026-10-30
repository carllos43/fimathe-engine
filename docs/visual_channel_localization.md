# Localização visual do Canal de Referência — Fimathe

## Objetivo

Este documento transforma em procedimento de análise visual as orientações legíveis no PDF enviado pelo usuário, sem substituir a base matemática que já existe no motor. A referência visual é o documento *Técnica Fimathe: Estratégias de Trading*, nas capturas das páginas internas 2/7 e 3/7. As capturas têm resolução limitada; por isso, este documento registra apenas o que está legível e não inventa regras ausentes.

## Regras extraídas do material visual

1. **Identificar a tendência antes de marcar o canal.** O exemplo mostrado é uma tendência de alta. A análise não deve escolher um canal antes de declarar qual movimento de preço está sendo interpretado.
2. **Marcar o Canal de Referência em uma região intermediária do movimento.** Não existe um número específico de pontos que determine um canal ideal; a escolha deve considerar as características do movimento mostrado.
3. **Pontos A e B representam regiões de negociação / suporte e resistência.** A IA deve explicar quais topos, fundos ou consolidações visíveis sustentam cada marcação.
4. **A marcação pode acompanhar o corpo ou a sombra dos candles.** A escolha depende do tamanho do canal pretendido. Não há regra numérica para decidir entre corpo e sombra.
5. **Evitar um canal estreito demais ou largo demais.** Critério qualitativo, não fórmula quantificada.
6. **Desenhar o Canal de Referência e a Zona Neutra como elementos distintos.** A geometria em `engine/channels/geometry.py` continua sendo a fonte dos cálculos.
7. **No exemplo de tendência de alta, observar a posição do último candle em relação ao nível de 50% do Canal de Referência.**
8. **No cenário de alta ilustrado, a compra é considerada após o retorno do preço e o rompimento do nível de 50% do Canal de Referência.** Não generalizar automaticamente para todos os cenários ou para tendência de baixa.
9. **Não tratar um toque ou pavio como confirmação de rompimento.** Confirmação exige fechamento de candle fora do canal (`B03` / `engine/breakouts/confirmation.py`).
10. **Explicar a localização.** Informar por que o canal foi escolhido, quais candles/regiões o sustentam, se foram usadas sombras ou corpos e por que uma alternativa foi rejeitada.

## Procedimento de leitura de um print

### Etapa A — Ler o gráfico sem antecipar uma operação
Registrar o que for realmente visível: ativo, timeframe, movimento analisado, legibilidade do eixo de preços, se os candles mais recentes parecem fechados. Não inventar preços exatos quando a escala não está legível.

### Etapa B — Propor o Canal de Referência
Registrar: limite inferior/superior estimados; ponto A e evidência; ponto B e evidência; escolha de corpo/sombra com justificativa; adequação qualitativa da largura (`adequada|estreita|larga|incerta`); alternativa plausível; confiança visual e limitações.

### Etapa C — Validar antes de calcular
- Verificar upper > lower.
- Amplitude com `channel_amplitude`.
- 50% com `level_50_of_channel`.
- Zona Neutra com `build_neutral_zone`, mantendo avisos provisórios.
- Não esconder ambiguidade quando dois canais cabem no gráfico.
- Não apresentar canal visual como “oficial”.

### Etapa D — Descrever a condição de entrada
Separar: canal identificado (hipótese + evidências); condição a esperar; confirmação (fechamento ou pendente); stop (com status); alvos/projeções (geométricos, não confirmados automaticamente).

## Formato de resposta para cada imagem

1. **Leitura do gráfico**
2. **Onde encontrei o canal** (A, B, evidências, corpo/sombra)
3. **Canal desenhado** (limites, amplitude, 50%, exact/estimated)
4. **Zona Neutra**
5. **Plano condicional** (o que precisa acontecer; estado atual)
6. **Stop e projeções**
7. **Alternativas e confiança**

## Política de segurança e rastreabilidade

- Educacional e de simulação; não envia ordens.
- Não fingir precisão numérica que a imagem não oferece.
- Separar regras confirmadas, interpretações e pendências.
- O PDF orienta a localização visual; a matemática permanece nos módulos existentes.
