# Pipeline visual de análise — etapa de integração

## O que foi acrescentado

- `engine/analysis/chart_pipeline.py`: recebe OHLC extraído por uma camada de visão e um candidato visual A/B; valida dados, calcula amplitude/50%/zona neutra e identifica rompimento apenas pelo fechamento de candle conhecido como fechado.
- `engine/analysis/svg_renderer.py`: cria um SVG com candles, Canal de Referência, Zona Neutra e nível de 50%, sem dependências externas.
- `tests/unit/test_chart_pipeline.py`: testes para entrada/stop não inventados, fechamento pendente, rompimento e renderização.

## Limite importante

Isto ainda **não lê pixels de uma imagem** nem desenha diretamente por cima do arquivo original. A etapa de visão precisa extrair os candles/escala e justificar o candidato de canal. O SVG reconstrói o gráfico a partir de OHLC e deve ser rotulado como reconstrução, não como sobreposição fiel do print. A precisão deve ser `exact`, `estimated` ou `unreadable` conforme a evidência.

## Por que não retorna entrada e stop numéricos automaticamente

A documentação do repositório reconhece que a construção A/B é parcialmente subjetiva e que não há gatilho universal confirmado para todos os cenários. A regra do stop diz que ele fica além do limite externo da Zona Neutra, mas não especifica um buffer numérico. Por isso, esta camada deixa entrada e stop pendentes até que uma variante de estratégia validada defina essas regras. Projeções continuam sendo projeções, nunca alvos confirmados automaticamente.

## Testes

```bash
python -m pytest tests/unit -v
```

## Para chegar ao fluxo automático no ChatGPT

O próximo componente é a integração que recebe a imagem, executa um modelo de visão para produzir o JSON de candles + candidato de canal, chama `analyze_chart_data` e devolve o SVG/texto no chat.
