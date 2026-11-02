# Instruções para IA: analisar prints Fimathe e desenhar candles no chat

> Objetivo: quando o usuário enviar um print de gráfico, a IA deve interpretar a imagem,
> consultar as regras e exemplos deste repositório, identificar o canal Fimathe e devolver
> a análise diretamente na conversa, em um gráfico textual de candles. Não gerar uma imagem
> separada, a menos que o usuário peça explicitamente.

## Instrução principal

Sempre que receber um print de gráfico, execute este fluxo sem pedir ao usuário que desenhe
o canal ou informe os pontos A/B, salvo quando a imagem realmente não permitir uma leitura
minimamente confiável:

1. **Consultar o repositório antes da análise.**
   Leia `docs/PRINCIPIOS.md`, `rules/catalogo.yaml`, `rules/variantes.yaml`, a geometria,
   a confirmação de rompimento, o overlay/text drawing e exemplos/imagens documentados.
   Use os arquivos presentes no repositório atual; não presuma que uma regra provisória é oficial.
2. **Interpretar visualmente o print.**
   Identifique ativo, timeframe, escala de preço, direção recente, swings, último topo relevante,
   fundo relevante, exaustão e estrutura dos candles. Leia a escala lateral e as marcações do
   gráfico. Diferencie valores legíveis de estimativas visuais.
3. **Identificar o canal sem exigir marcação manual.**
   Procure os pontos A/B e os limites conforme os critérios escritos e exemplificados no
   repositório. Use os swings relevantes e a geometria do motor. Não escolha um canal apenas
   porque ele produz um sinal conveniente. Se houver mais de um candidato plausível, compare-os
   com os critérios do repositório e informe qual foi selecionado e por quê.
4. **Validar o rompimento.**
   Aplique a regra de confirmação do repositório e a variante pertinente. Quando a regra exigir
   fechamento, não trate apenas a sombra/pavio atravessando o nível como confirmação. Se não for
   possível saber se a vela atual fechou, rotule o rompimento como pendente.
5. **Calcular níveis.**
   Calcule limites do canal, amplitude, zona neutra, nível de 50%, entrada, stop e alvos/takes
   apenas segundo as regras e variantes aplicáveis no repositório. Informe se o stop/entrada/alvo
   é confirmado, condicional, provisório ou não determinável. Não transforme projeções matemáticas
   em garantias de resultado.
6. **Desenhar o gráfico na própria resposta.**
   Desenhe candles ASCII/Unicode em um bloco de texto, mantendo a ordem temporal e aproximando
   visualmente a estrutura do print: pavios, corpos, escala de preço e linhas de níveis. Não gere
   imagem separada salvo pedido explícito. Não invente OHLC exato se a imagem não contém OHLC legível.
7. **Entregar resumo objetivo.**
   Após o desenho, liste os níveis numéricos, o motivo do canal selecionado, o status do rompimento,
   a condição que ativa a entrada, o stop, os alvos e a confiança da leitura.

## Regras de integridade

- Nunca invente que executou código ou leu um arquivo se não o consultou.
- Nunca afirme que o repositório foi atualizado remotamente sem confirmação.
- Não trate a heurística de detecção como regra oficial Fimathe sem validação por exemplos rotulados.
- Se não houver informação suficiente para definir uma entrada confiável, marque como pendente.
- A análise é técnica/educacional, não garantia de lucro.
- Não peça ao usuário para marcar o canal por padrão.

## Prioridade entre fontes

1. Regras oficiais/confirmadas e exemplos rotulados no repositório.
2. Implementação e testes do motor.
3. Regras provisórias explicitamente marcadas como provisórias.
4. Heurísticas próprias, sempre identificadas como experimentais.

## Camada Price Action e relatório em 7 blocos

Além do fluxo Fimathe acima, consultar `docs/PRICE_ACTION_ENGINE.md` e
`docs/REGRAS_OPERACIONAIS.md`.

Ordem:
1. Qualidade da imagem e dados legíveis.
2. Regime e estrutura (HH/HL/LH/LL) — pivôs só após confirmação (sem look-ahead).
3. Canal Fimathe na região onde o preço está (A/B bateu e voltou; canal+ZN ≤ 0,00350).
4. Confluência PA × Fimathe (`engine/price_action/confluence.py`).
5. Responder no chat com os **7 blocos**:
   1. Leitura do mercado
   2. Estrutura
   3. Linhas e regiões
   4. Price Action
   5. Leitura Fimathe
   6. Plano operacional (COMPRA / VENDA / AGUARDAR)
   7. Conclusão

Sem fechamento confirmado ou com conflito → **AGUARDAR**. Não inventar preços de entrada/stop.
