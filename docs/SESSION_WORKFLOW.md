# Fluxo profissional de análise — continuidade e memória

## Objetivo

Não reiniciar a análise a cada print. Toda leitura de gráfico:
1. consulta o que já está registrado no repositório;
2. dá continuidade ao canal / bias / plano da sessão ativa;
3. só abre **nova** análise estrutural quando a anterior for invalidada ou a semana mandar reset.

## Cadência semanal

| Quando | O que fazer |
|--------|-------------|
| **Domingo ou segunda** | Análise de contexto da **semana** (H1/H4 se disponível + M15 operacional). Gravar em `analysis/weekly/YYYY-WNN.md` e atualizar `docs/sessions/<ATIVO>/CURRENT.md`. |
| **Durante a semana** | Cada print = **checagem + atualização** do `CURRENT.md`, não análise do zero. |
| **Take / parcial** | Registrar no log da sessão; não “picar” alvos fora do plano semanal. |
| **Stop / inválido** | Marcar invalidação, aplicar regra Fimathe do PDF (nova venda na sequência ou compra no retorno) e gravar o que mudou. |

## A cada print que o usuário enviar

1. **Ler** `docs/sessions/<ATIVO>/CURRENT.md` (se existir).
2. **Ler** última entrada do log da sessão.
3. **Comparar** preço atual com L / H / ZN / stop / bias gravados.
4. **Classificar o estado:** `DENTRO_DO_PLANO` | `GATILHO_ATINGIDO` | `EM_OPERACAO` | `INVALIDADO` | `NOVA_SEMANA`.
5. **Responder** no formato 7 blocos, citando o histórico.
6. **Gravar** de volta (`CURRENT.md` + linha no log).

## Hierarquia de decisão

1. Plano semanal ativo (se ainda válido).
2. Sessão `CURRENT.md` do ativo.
3. Regras Fimathe (`docs/REGRAS_OPERACIONAIS.md`) + PDF.
4. Price Action (`docs/PRICE_ACTION_ENGINE.md`).
5. Nova análise completa **somente** se invalidado ou sem histórico.

## O que nunca fazer

- Redesenhar canal do zero ignorando `CURRENT.md`.
- Tratar cada print como mercado novo.
- Inventar entrada/stop sem amarrar ao plano gravado.
- Apagar histórico de níveis — só arquivar quando a semana fechar.

## Estrutura de arquivos

```text
docs/sessions/<ATIVO>/CURRENT.md
docs/sessions/<ATIVO>/log.md
analysis/weekly/YYYY-WNN.md
```
