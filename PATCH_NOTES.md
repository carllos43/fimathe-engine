# Atualização incremental — localização visual do Canal de Referência

## Arquivos incluídos
- `docs/visual_channel_localization.md`: procedimento de localização derivado das capturas legíveis do PDF.
- `rules/visual_channel_localization.yaml`: regras visuais estruturadas e seus estados.
- `docs/image_analysis_contract.md`: contrato de integração para imagem → motor → gráfico anotado e resposta no chat.
- `examples/chart_image_analysis_prompt.md`: instrução reutilizável para a aplicação que recebe prints.
- `engine/channels/visual_assessment.py`: valida o candidato visual e calcula amplitude, 50% e Zona Neutra com as funções existentes.
- `tests/unit/test_visual_assessment.py`: testes para o módulo novo.

## Como aplicar
Copie os diretórios/arquivos para a raiz do repositório, preservando os caminhos. Nenhum arquivo existente é substituído.

## Testes
Execute na raiz do repositório:

```bash
python -m pytest tests/unit -v
```

## Limite importante
O módulo novo não interpreta pixels. Ele recebe o candidato de canal identificado pela IA de visão, valida os dados e reutiliza a geometria existente. A extração visual da imagem e a renderização anotada sobre o print original precisam ser conectadas pela aplicação. Adicionar estes arquivos ao GitHub não faz o ChatGPT consultar o repositório automaticamente em qualquer conversa sem uma integração configurada.
