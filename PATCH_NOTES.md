# Patch — pipeline visual v0.3 (proposta)

Adiciona uma primeira camada executável entre visão e motor matemático: valida OHLC, calcula níveis usando as funções existentes, deixa explícito quando o rompimento depende de candle fechado e produz SVG de candles com linhas do canal.

Este patch não substitui o motor existente e não contém extração de pixels. Não muda regras Fimathe nem transforma heurísticas em regras oficiais. Entrada e stop permanecem sem preço enquanto o repositório não definir um gatilho universal e a margem exata do stop.

Inclua os arquivos mantendo a estrutura de diretórios. Depois rode `python -m pytest tests/unit -v`.
