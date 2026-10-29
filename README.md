# Fimathe – Motor Educacional e de Simulação

> **AVISO IMPORTANTE**  
> Este repositório é **exclusivamente educacional e de simulação**.  
> Não executa ordens reais, não se conecta a corretoras e **não promete nenhum resultado financeiro**.  
> A técnica Fimathe pertence a Marcelo Ferreira. Este projeto apenas documenta e modela as regras publicamente disponíveis de forma rastreável, para estudo e validação de lógica.  
> Trading envolve risco elevado de perda de capital. Use por sua conta e risco.

## Objetivo

Criar um motor determinístico que:
1. Representa fielmente as regras extraídas das fontes disponíveis.
2. Separa **fato confirmado** de **decisão de projeto** e de **lacuna**.
3. Permite simulação de candles sem execução real.
4. Facilita a validação visual contra os gráficos originais (quando os prints forem fornecidos).

## Status atual – v0.2

**Motor matemático implementado** (funções puras + modelos tipados + testes).  
Ainda **sem** execução de ordens e sem interface gráfica de trading.

| Variante              | Fonte principal      | Status no repositório          |
|-----------------------|----------------------|--------------------------------|
| Aula H1/M15 (pontos A/B) | Doc A (P1–P10)     | Regras catalogadas             |
| Raiz / Zona Neutra    | Transcrições 1-2     | Geometria + testes             |
| Teoria dos Ciclos     | Transcrições + Doc B | Expansões plugáveis (fórmula C1–C4 ainda provisional) |
| PCM                   | Doc B §6             | Regras provisórias             |
| Mapeamento superior + fatiamento | Transcrição 3 | Implementado (“Fimathe 350” math pending) |

### Como rodar os testes

```bash
cd fimathe-repo
python -m pytest tests/unit -v
```

### Documentação nova
- `docs/mathematical_engine.md`
- `docs/fimathe_rules.md`
- `docs/sources/fimathe_transcription.md`

## Estrutura do repositório

```
fimathe-repo/
├── README.md
├── docs/
├── rules/
├── engine/
├── tests/
├── examples/
└── data/
```

## Princípios

- Toda regra aponta para um ID e uma fonte.
- Nenhuma regra inventada.
- Determinismo: mesma sequência de candles → mesmo resultado.
- Sem execução real de ordens.

## Licença e direitos

- Conteúdo educacional derivado de material público.
- **Não copie os PDFs originais** para dentro do repositório.
- Cite sempre a fonte e o autor (Marcelo Ferreira / Fimathe).
