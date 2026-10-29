# Patch de instruções para análise automática de prints Fimathe

Este pacote torna explícito, dentro do repositório, o comportamento esperado de uma IA que tenha
acesso aos arquivos do projeto:

- ler as regras e exemplos;
- interpretar o print sem pedir ao usuário para traçar o canal;
- localizar swings e escolher canal conforme a metodologia documentada;
- calcular entrada, stop e takes segundo as regras/variantes;
- desenhar candles com ASCII/Unicode diretamente no chat, sem gerar imagem separada;
- declarar incerteza quando o print ou as regras não sustentarem um nível exato.

## Arquivos

- `AGENTS.md`: instruções curtas para agentes de IA que leem o repositório.
- `AI_CHART_WORKFLOW.md`: fluxo completo de análise.
- `docs/AI_CHART_RESPONSE_TEMPLATE.md`: formato de resposta textual.

## Como instalar

Extraia este ZIP na raiz de `carllos43/fimathe-engine` e adicione os arquivos ao repositório.
Não substitua os arquivos atuais. Faça commit e push. Em seguida, a IA que tiver acesso ao
repositório deve ler `AGENTS.md` e `AI_CHART_WORKFLOW.md`.

## Limitação importante

Estes arquivos são instruções persistentes, não treinamento do modelo nem garantia de que toda IA
os carregará automaticamente. O agente precisa ter acesso ao repositório e seguir as instruções.
A metodologia deve ser validada contra exemplos do projeto; regras incompletas não podem ser
transformadas em certezas.
