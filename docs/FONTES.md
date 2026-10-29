# FONTES.md – Inventário e confiabilidade

## Fontes utilizadas neste repositório (v0.1)

### Doc A – Primária (parcial)
- **Título:** Aplicação da Técnica Fimathe no Forex
- **Tipo:** Anotações de aula (≈10 páginas)
- **Formato disponível:** PDF de 1 página física contendo collage de previews do Scribd
- **Confiabilidade:** Alta para as partes legíveis do texto. Baixa para gráficos (imagens de baixa resolução + anúncios).
- **Referências internas:** P1 a P10 (páginas do material original)
- **O que foi extraído:** Timeframes por estilo, pontos A/B, projeção, 50%/100%, exaustão ≈85%, TP 80-100%, stop no TF menor, triângulo de 2 níveis, risco 3%, regras básicas.

### Doc B – Secundária (ausente no ambiente)
- **Título declarado:** Fimathe: Teoria dos Ciclos, Estudo Completo (≈16 páginas)
- **Tipo:** Compilação descrita como “aprimorada por IA”, com referências a vídeos e links promocionais
- **Confiabilidade:** Média-baixa. Não é material primário do autor. Afirmações de “alta probabilidade” não têm evidência no texto.
- **Status:** Arquivo **não fornecido**. Regras B01–B24 estão no relatório de requisitos apenas como provisórias.
- **Risco:** Implementar regras do Doc B como se fossem oficiais pode introduzir paráfrases incorretas.

### Material oficial de Marcelo Ferreira
- Canal YouTube oficial (~447k inscritos)
- Conceitos confirmados publicamente: Teoria dos Ciclos, Canal de Abertura (4 velas M15), PCM, Linha de Equador, Zona Neutra.
- Este repositório **não transcreve** vídeos. Qualquer regra derivada de vídeo oficial precisará de timestamp + confirmação visual.

## Política de uso das fontes

1. Regras só entram no catálogo oficial se tiverem evidência em Doc A legível ou em material primário confirmado.
2. Regras do Doc B ficam marcadas como `provisoria` até o PDF original + imagens serem fornecidos.
3. Nunca copiar o PDF inteiro para o repositório.
4. Toda regra futura no código terá campo `fonte: "DocA:P3"` ou `fonte: "DocB:§3.2"` ou `fonte: "decisao-projeto"`.

## Histórico de auditoria

- 2026-10-29: Auditoria completa do Doc A (texto extraído + lacunas de gráficos).
- 2026-10-29: Relatório de requisitos do repositório criado com base nos dois documentos (Doc B ainda ausente).
