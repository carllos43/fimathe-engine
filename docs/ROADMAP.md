# ROADMAP.md

| Fase | Entrega                                      | Critério de pronto                                      | Status atual |
|------|----------------------------------------------|---------------------------------------------------------|--------------|
| 0    | Documentação + catálogo de regras            | Regras com ID/fonte; lacunas listadas                   | **Concluída** |
| 1    | Geometria e canais                           | Testes de canal, altura, projeção, 50%/100%             | Pendente (precisa prints) |
| 2    | Ciclos e confirmação por fechamento          | CA/C1 corretos; modelo de ciclos plugável               | Pendente (precisa Doc B + prints) |
| 3    | Gestão de stop e alvos                       | 0x0, subciclos, trailing, T1/T2 ou 80-100%              | Pendente |
| 4    | Fatiamento multi-timeframe                   | Reamostragem validada; contexto top-down                | Pendente |
| 5    | Máquina de estados + simulador               | Execução determinística de uma semana completa          | Pendente |
| 6    | Virada de mão e PCM (se no escopo)           | Regras B15/B16 testadas                                 | Pendente |
| 7    | Validação com imagens e exemplos             | Casos de ouro reproduzidos; pendências fechadas         | Pendente |

**Regra de ouro:** nenhuma fase de código começa enquanto a fase anterior de documentação/validação visual não estiver fechada ou explicitamente marcada como “decisão de projeto”.
