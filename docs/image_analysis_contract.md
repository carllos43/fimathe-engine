# Contrato de integração: imagem de gráfico → Fimathe Engine → resposta no chat

## Finalidade

Este contrato define como uma integração de IA com visão deve usar o repositório quando o usuário enviar um print de gráfico. Ele complementa a base técnica existente; não cria um motor paralelo.

**Importante:** colocar este arquivo no GitHub não faz, por si só, o ChatGPT consultar o repositório automaticamente em todas as conversas. A aplicação que recebe a imagem precisa buscar/embutir estas instruções e executar o motor Python. Sem essa integração, o documento funciona como especificação de comportamento.

## Fluxo obrigatório

1. Carregar as regras existentes em `rules/catalogo.yaml` e `docs/fimathe_rules.md`, além de `rules/visual_channel_localization.yaml` e `docs/visual_channel_localization.md`.
2. Usar visão computacional para interpretar a imagem. Não afirmar que os preços são exatos quando a escala não permite lê-los.
3. Identificar o candidato de Canal de Referência (pontos A/B) com evidência visual e precisão (`exact|estimated|unreadable`).
4. Passar o candidato ao módulo `engine/channels/visual_assessment.py` para validação geométrica.
5. Usar `engine/channels/geometry.py` para amplitude, zona neutra e 50%.
6. Usar `engine/breakouts/confirmation.py` quando houver vela fechada verificável.
7. Usar `engine/analysis/chart_overlay.py` / `text_draw.py` para o pacote de marcações e desenho textual.
8. Separar claramente: “estimado”, “pendente” e “confirmado”.
9. Responder no chat com resumo textual, justificativa do canal, condição de entrada, estado de confirmação, stop e limitações.
10. Registrar as regras/versões usadas para reprodutibilidade.

## Formato de dados sugerido (IA de visão → motor)

```json
{
  "symbol": null,
  "timeframe": null,
  "trend": {
    "direction": "up|down|sideways|unknown",
    "evidence": "descrição visual",
    "status": "confirmed|probable|pending|invalid"
  },
  "channel_candidate": {
    "lower": null,
    "upper": null,
    "price_precision": "exact|estimated|unreadable",
    "point_a_evidence": "região/candles que justificam A",
    "point_b_evidence": "região/candles que justificam B",
    "boundary_method": "body|wick|mixed|uncertain",
    "width_assessment": "appropriate|narrow|wide|uncertain",
    "alternatives": []
  },
  "latest_candle": {
    "closed": null,
    "close_price": null,
    "timestamp": null
  },
  "image_limitations": []
}
```

Campos nulos são intencionais: não preencher o que a imagem não revela.

## Regras para o texto ao usuário

- Dizer “identifiquei este candidato de canal porque…” e apontar A/B.
- Se houver duas marcações plausíveis, apresentar ambas ou explicar a preferência.
- Separar “condição de entrada” de “entrada confirmada”.
- Não afirmar rompimento confirmado sem fechamento verificável.
- Mostrar projeções como projeções, nunca como alvos garantidos.
- Não ocultar warnings de regras provisórias do motor.

## Integração real necessária

A aplicação precisa: receber a imagem; disponibilizar este contrato e as regras ao modelo de visão; executar o código Python do motor; combinar resultado matemático com interpretação visual; devolver a resposta no chat.
