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

## Desenho de candles em texto

Convenção:
- `▉` candle de alta (close >= open)
- `▏` candle de baixa (close < open)
- `│` pavio
- `═` limite do canal
- `┄` nível projetado/50%/entrada/alvo
- `─` stop
- `→` eixo do tempo

Exemplo de apresentação (somente formato; valores ilustrativos):

```text
EUR/USD · M15 · leitura visual do print

1.1180 │          │                   ┄ T1
1.1170 │       │  ▉
1.1160 │    │  ▉  ▏  │
1.1150 ╪═════════════════════════════ H / entrada condicional
1.1140 │  │ ▏  ▉       │
1.1130 │    ▉    │              ┄ 50%
1.1120 ╪═════════════════════════════ L
1.1110 │                    ─ STOP
       └─────────────────────────────→ tempo

Canal: ...
Rompimento: ...
Entrada: ...
Stop: ...
T1/T2: ...
Confiança: ...
```

O desenho deve refletir a estrutura visível do print enviado, não copiar cegamente este exemplo.
Se não houver dados OHLC exatos, os corpos e pavios são aproximações visuais; os níveis devem ser
rotulados como estimados quando a escala não permitir leitura precisa.

## Regras de integridade

- Nunca invente que executou código ou leu um arquivo se não o consultou.
- Nunca afirme que o repositório foi atualizado remotamente sem confirmação.
- Não trate a heurística de detecção como regra oficial Fimathe sem validação por exemplos rotulados.
- Se os arquivos tiverem regras conflitantes, explique o conflito e priorize a regra marcada como
  confirmada/oficial segundo a documentação do projeto.
- Se não houver informação suficiente para definir uma entrada confiável, ainda desenhe a leitura
  visual e mostre os candidatos, mas marque entrada como pendente/em espera em vez de inventar
  um sinal confirmado.
- A análise é técnica/educacional, não garantia de lucro.
- Não peça ao usuário para marcar o canal por padrão. A IA deve tentar interpretá-lo primeiro.

## Prioridade entre fontes

1. Regras oficiais/confirmadas e exemplos rotulados no repositório.
2. Implementação e testes do motor.
3. Regras provisórias explicitamente marcadas como provisórias.
4. Heurísticas próprias, sempre identificadas como experimentais.

Se o repositório não definir como escolher pontos A/B em um cenário, documente a lacuna. Pode
propor um candidato visual, mas não o rotule como oficialmente confirmado.
