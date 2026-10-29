# Modelo de resposta da IA para um print de gráfico

Use esta estrutura quando o usuário enviar um print. Não copie os valores do exemplo; leia o print
real e consulte as regras atuais do repositório.

```text
[ATIVO] · [TIMEFRAME] · [candles visualmente interpretados]

[escala de preço] │ [pavios e corpos dos candles] [T1/T2]
[escala de preço] ╪═══════════════════════════ [limite superior / gatilho]
[escala de preço] │ [pavios e corpos dos candles]
[escala de preço] │ [candle(s) recente(s)]      ┄ 50%
[escala de preço] ╪═══════════════════════════ [limite inferior]
[escala de preço] │                            ─ STOP
                  └──────────────────────────→ tempo
```

Em seguida, informe:
- Canal selecionado e evidência visual dos pontos A/B.
- Amplitude, zona neutra e nível de 50%, se a regra aplicável os define.
- Estado do rompimento: não ocorrido / intrabar / confirmado no fechamento / não verificável.
- Entrada: preço e condição de ativação.
- Stop: preço e regra/variante utilizada.
- Alvos/takes: preços, regra de projeção e se são oficiais ou provisórios.
- Confiança e limitações de leitura do print.

O desenho é textual e esquemático. Deve preservar o formato visual de candles e a estrutura de mercado
que aparece no print, mas não deve alegar valores OHLC exatos quando estes não estão disponíveis.
