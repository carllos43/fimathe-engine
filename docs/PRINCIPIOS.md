# PRINCIPIOS.md – Princípios de projeto

Estes princípios valem para **todo** o repositório e para qualquer código futuro.

1. **Rastreabilidade**  
   Toda regra implementada aponta para um ID (R01, B03…) e uma fonte (página/seção).  
   Nenhuma regra “órfã”.

2. **Variantes explícitas**  
   Raiz, Aula H1/M15, Teoria dos Ciclos e PCM são conjuntos de regras diferentes.  
   Não misturar numa única lógica.

3. **Fato vs escolha**  
   Separar claramente:
   - Confirmado pela fonte
   - Inferência (com nível de confiança)
   - Decisão de projeto (quando a fonte é omissa)

4. **Determinismo**  
   Mesma sequência de candles + mesmos parâmetros → mesmo resultado, sempre.

5. **Sem execução real**  
   Apenas leitura de candles e simulação. Nenhuma ordem real, nenhum login em corretora.

6. **Não inventar**  
   Onde faltar regra, o código expõe parâmetro configurável e marca como “decisão do projeto” ou “pendente”.

7. **Testes de fidelidade, não de lucratividade**  
   Os testes verificam se a regra foi seguida. Backtest de performance **não** é critério de validação do motor.

8. **Imagens primeiro**  
   Casos de ouro só são criados depois de ver os gráficos originais. Sem imagem = teste marcado como pendente.
